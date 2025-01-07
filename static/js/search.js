document.addEventListener("DOMContentLoaded", function () {
  const searchBar = document.getElementById("search_bar");
  const searchButton = document.getElementById("searchButton");
  const filterSelect = document.getElementById("filter");
  const mealsSection = document.querySelector(".meals");
  const prevPage = document.getElementById("prevPage");
  const nextPage = document.getElementById("nextPage");
  const pageNumbers = document.getElementById("pageNumbers");
  let currentPage = 1;
  let totalPages = 1;
  const itemsPerPage = 8; // here pagination

  async function performSearch() {
    const query = searchBar.value;
    const restaurant = filterSelect.value;

    try {
      const response = await fetch(
        `/api/v1/search?query=${encodeURIComponent(
          query
        )}&restaurant=${encodeURIComponent(restaurant)}&page=${currentPage}`
      );
      const data = await response.json();

      updateMealsSection(data.meals);
      updatePagination(data.total);
    } catch (error) {
      console.error("Search failed:", error);
    }
  }

  function sanitizeName(name) {
    return name.replace(/\s+/g, '_');
  }

  async function findImage(basePath, fileName) {
    const extensions = ['jpeg', 'jpg', 'png'];
    for (const ext of extensions) {
        try {
            const response = await fetch(`../static/images/menu_items/${basePath}/${fileName}.${ext}`);
            if (response.ok) {
                return `${fileName}.${ext}`;
            }
        } catch (error) {
            continue;
        }
    }
    return 'default.png'; // Fallback image
  }

  async function updateMealsSection(meals) {
    const mealElements = await Promise.all(meals.map(async (meal) => {
        const imagePath = await findImage(
            sanitizeName(meal.restaurant_name),
            sanitizeName(meal.name)
        );

        return `
            <div class="meal" data-meal-id="${meal.id}">
                <img src="../static/images/menu_items/${sanitizeName(meal.restaurant_name)}/${imagePath}"
                     alt="${meal.name}"
                     onerror="this.src='../static/images/default.png'" />
                <hr />
                <div class="meal-info">
                    <h3>${meal.name}</h3>
                    <div class="meal-footer">
                        <span class="price" data-price="${meal.price}">$${meal.price}</span>
                        <div class="quantity">
                            <img src="../static/images/reduce.png" class="decrease" alt="Reduce quantity" />
                            <span class="quantity-value" data-quantity="0">0</span>
                            <img src="../static/images/add.png" class="increase" alt="Increase quantity" />
                        </div>
                    </div>
                </div>
            </div>
        `;
    }));

    mealsSection.innerHTML = mealElements.join('');
    attachQuantityListeners();
  }

  function attachQuantityListeners() {
    const meals = document.querySelectorAll('.meal');
    meals.forEach(meal => {
        const decreaseBtn = meal.querySelector('.decrease');
        const increaseBtn = meal.querySelector('.increase');
        const quantitySpan = meal.querySelector('.quantity-value');

        decreaseBtn.addEventListener('click', () => {
            let quantity = parseInt(quantitySpan.getAttribute('data-quantity'));
            if (quantity > 0) {
                quantity--;
                quantitySpan.setAttribute('data-quantity', quantity);
                quantitySpan.textContent = quantity;
            }
        });

        increaseBtn.addEventListener('click', () => {
            let quantity = parseInt(quantitySpan.getAttribute('data-quantity'));
            quantity++;
            quantitySpan.setAttribute('data-quantity', quantity);
            quantitySpan.textContent = quantity;
        });
    });
  }

  function updatePagination(totalItems) {
    totalPages = Math.ceil(totalItems / itemsPerPage);

    // Don't show pagination if only one page
    if (totalPages <= 1) {
      document.querySelector(".pagination").style.display = "none";
      return;
    }

    document.querySelector(".pagination").style.display = "flex";

    // Update page numbers display
    let pagesHtml = "";
    for (let i = 1; i <= totalPages; i++) {
      // Here Pagination
      if (totalPages > 7) {// here pagination -1
        // Show ellipsis for many pages
        if (
          i === 1 ||
          i === totalPages ||
          (i >= currentPage - 1 && i <= currentPage + 1)
        ) {
          pagesHtml += `<span class="page-number ${
            i === currentPage ? "active" : ""
          }"
                                       data-page="${i}">${i}</span>`;
        } else if (i === currentPage - 2 || i === currentPage + 2) {
          pagesHtml += '<span class="ellipsis">...</span>';
        }
      } else {
        pagesHtml += `<span class="page-number ${
          i === currentPage ? "active" : ""
        }"
                                   data-page="${i}">${i}</span>`;
      }
    }
    pageNumbers.innerHTML = pagesHtml;

    // Update prev/next buttons state
    prevPage.classList.toggle("disabled", currentPage === 1);
    nextPage.classList.toggle("disabled", currentPage === totalPages);
  }

  // Event listeners
  searchButton.addEventListener("click", performSearch);
  searchBar.addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
      performSearch();
    }
  });
  filterSelect.addEventListener("change", performSearch);

  // Pagination event listeners
  prevPage.addEventListener("click", function (e) {
    e.preventDefault();
    if (currentPage > 1) {
      currentPage--;
      performSearch();
    }
  });

  nextPage.addEventListener("click", function (e) {
    e.preventDefault();
    if (currentPage < totalPages) {
      currentPage++;
      performSearch();
    }
  });

  // Initial search
  performSearch();
});
