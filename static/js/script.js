/**
 * @file Main script for cart management and UI interactions
 */

/** @type {Array<{id: string, name: string, price: number, quantity: number}>} */
let cartItems = [];

/**
 * Updates cart with new item or quantity
 * @param {string} mealId - Meal identifier
 * @param {string} mealName - Meal name
 * @param {number} mealPrice - Meal price
 * @param {'increase'|'decrease'} action - Action to perform
 * @returns {Promise<void>}
 */
const updateCart = async (mealId, mealName, mealPrice, action) => {
  try {
    const response = await fetch("/api/v1/cart/update", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ menu_item_id: mealId, action }),
    });

    if (!response.ok) throw new Error("Failed to update cart");

    const data = await response.json();
    updateLocalCart(data);
    updateCartDisplay();
    showToast("Cart updated successfully", "success");
  } catch (error) {
    console.error("Error updating cart:", error);
    showToast("Failed to update cart", "error");
  }
};

// Meal elements event handling
const mealElements = document.querySelectorAll(".meal");

mealElements.forEach((mealElement) => {
  const { mealId, mealName, mealPrice } = {
    mealId: mealElement.dataset.mealId,
    mealName: mealElement.querySelector("h3")?.textContent ?? "",
    mealPrice: parseFloat(
      mealElement.querySelector(".price")?.dataset.price ?? "0"
    ),
  };

  const quantityElement = mealElement.querySelector(".quantity-value");

  const decreaseButton = mealElement.querySelector(".decrease");
  const increaseButton = mealElement.querySelector(".increase");

  async function updateQuantity(action) {
    // Check if user is logged in
    const isLoggedIn = document.body.classList.contains("user-logged-in");
    if (!isLoggedIn) {
      localStorage.setItem(
        "pendingCartAction",
        JSON.stringify({ mealId, action })
      );
      window.location.href = "/login";
      return;
    }
    await updateCart(mealId, mealName, mealPrice, action);
  }

  increaseButton.addEventListener("click", () => updateQuantity("increase"));
  decreaseButton.addEventListener("click", () => updateQuantity("decrease"));
});

/**
 * Updates the cart display with current items
 * @returns {void}
 */
const updateCartDisplay = () => {
  const cartCount = document.getElementById("cart-count");
  if (!cartCount) return;

  const totalQuantity = cartItems.reduce(
    (total, item) => total + item.quantity,
    0
  );
  cartCount.textContent = totalQuantity.toString();
  cartCount.classList.toggle("cart-count-active", totalQuantity > 0);
};

function updateLocalCart(data) {
  if (data.order) {
    const itemIndex = cartItems.findIndex((item) => item.id === data.item.id);
    if (itemIndex !== -1) {
      if (data.item.quantity > 0) {
        cartItems[itemIndex].quantity = data.item.quantity;
      } else {
        cartItems.splice(itemIndex, 1);
      }
    } else if (data.item.quantity > 0) {
      cartItems.push(data.item);
    }
  } else {
    cartItems = [];
  }
}

// Toast notification function
function showToast(message, type) {
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.textContent = message;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.classList.add("show");
    setTimeout(() => {
      toast.classList.remove("show");
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }, 100);
}

// Modal functionality
const modal = {
  element: /** @type {HTMLElement|null} */ (document.querySelector(".modal")),
  knowMoreBtn: /** @type {HTMLElement|null} */ (
    document.querySelector(".know_more")
  ),
  closeBtn: /** @type {HTMLElement|null} */ (document.querySelector(".close")),
};

if (modal.knowMoreBtn && modal.element) {
  modal.knowMoreBtn.addEventListener("click", () => {
    modal.element?.classList.add("show");
    modal.element?.classList.remove("fade-out");
  });
}

// Add event listener to close the modal when the close button is clicked
modal.closeBtn?.addEventListener("click", () => {
  modal.element?.classList.add("fade-out");
  setTimeout(() => {
    modal.element?.classList.remove("show", "fade-out");
  }, 400);
});

// Add event listener to close the modal if the user clicks outside of it
window.addEventListener("click", (e) => {
  if (e.target === modal.element) {
    modal.element?.classList.add("fade-out");
    setTimeout(() => {
      modal.element?.classList.remove("show", "fade-out");
    }, 400);
  }
});

const element = document.getElementById("elementId");
if (element) {
  element.addEventListener("click", handler);
}
