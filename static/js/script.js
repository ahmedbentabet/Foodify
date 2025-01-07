// Defining the selected meals in the cart
let cartItems = []; // Array to store meals and quantities in the cart

// Function to update the cart (quantity only)
async function updateCart(mealId, mealName, mealPrice, quantityChange) {
    try {
        const response = await fetch('/api/v1/orders/update_item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                meal_id: mealId,
                quantity_change: quantityChange
            })
        });

        if (!response.ok) {
            throw new Error('Failed to update cart');
        }

        const data = await response.json();
        
        // Update local cart state only after successful API call
        const existingItemIndex = cartItems.findIndex(item => item.id === mealId);

        if (existingItemIndex !== -1) {
            const existingItem = cartItems[existingItemIndex];
            existingItem.quantity += quantityChange;
            if (existingItem.quantity <= 0) {
                cartItems.splice(existingItemIndex, 1);
            }
        } else if (quantityChange > 0) {
            cartItems.push({
                id: mealId,
                name: mealName,
                price: mealPrice,
                quantity: quantityChange
            });
        }

        // Update the cart display
        updateCartDisplay();

    } catch (error) {
        console.error('Error updating cart:', error);
        alert('Failed to update cart. Please try again.');
        
        // Revert the UI change
        const quantityElement = document.querySelector(`.meal[data-meal-id="${mealId}"] .quantity-value`);
        if (quantityElement) {
            const currentQuantity = parseInt(quantityElement.getAttribute('data-quantity')) - quantityChange;
            quantityElement.setAttribute('data-quantity', currentQuantity);
            quantityElement.textContent = currentQuantity;
        }
    }
}

// Function to update the cart display (showing only the number of meals in the nav bar)
function updateCartDisplay() {
    const cartCount = document.getElementById('cart-count');

    // Calculate the total number of meals in the cart
    const totalQuantity = cartItems.reduce((total, item) => total + item.quantity, 0);

    // Update the number of items in the cart in the nav bar
    cartCount.textContent = totalQuantity;
    cartCount.classList.remove('cart-count-hidden');
    cartCount.style.backgroundColor = totalQuantity > 0 ? 'red' : 'transparent';
}

// Identifying the buttons affecting the meals
const mealElements = document.querySelectorAll('.meal');

// Adding event listeners to the buttons for each meal
mealElements.forEach(mealElement => {
    const mealId = mealElement.getAttribute('data-meal-id');
    const mealName = mealElement.querySelector('h3').textContent;
    const mealPrice = parseFloat(mealElement.querySelector('.price').getAttribute('data-price'));
    const quantityElement = mealElement.querySelector('.quantity-value');

    const decreaseButton = mealElement.querySelector('.decrease');
    const increaseButton = mealElement.querySelector('.increase');

    // Decrease quantity
    decreaseButton.addEventListener('click', () => {
        let quantity = parseInt(quantityElement.getAttribute('data-quantity'));
        if (quantity > 0) {
            quantity -= 1;
            quantityElement.setAttribute('data-quantity', quantity);
            quantityElement.innerText = quantity;
            updateCart(mealId, mealName, mealPrice, -1); // Decrease quantity in the cart by 1
        }
    });

    // Increase quantity
    increaseButton.addEventListener('click', () => {
        let quantity = parseInt(quantityElement.getAttribute('data-quantity'));
        quantity += 1; // Increase quantity by 1
        quantityElement.setAttribute('data-quantity', quantity);
        quantityElement.innerText = quantity;
        updateCart(mealId, mealName, mealPrice, 1); // Increase quantity in the cart by 1
    });
});

// Function to update the cart display (showing only the number of meals in the nav bar)
function updateCartDisplay() {
        const cartCount = document.getElementById('cart-count');

        // Calculate the total number of meals in the cart
        const totalQuantity = cartItems.reduce((total, item) => total + item.quantity, 0);

        if (totalQuantity > 0) {
            // If the quantity is greater than zero, show a red badge
            if (!cartCount) {
                // If the element does not exist, add it to the DOM
                const span = document.createElement('span');
                span.id = 'cart-count';
                span.classList.remove('cart-count-hidden'); // Remove the hidden class
                span.style.backgroundColor = 'red'; // Add red background color
                span.style.color = 'white'; // Change the color to white for the number
                span.style.padding = '0.2em'; // Add padding to show the badge
                span.style.borderRadius = '50%'; // Make the badge circular
                document.querySelector('.cart-icon-container a').appendChild(span);  // Add it to the link
            }
        } else {
            // If the quantity is zero, remove the element completely
            if (cartCount) {
                cartCount.remove();
            }
        }
    }

    // Call the function to update the cart
    updateCartDisplay();


//================================================================================================
// Modal functionality
const knowMoreButton = document.querySelector('.know_more'); // Button to open the modal
const modal = document.querySelector('.modal'); // Modal container
const closeModal = document.querySelector('.close'); // Close button inside the modal

// Add event listener to open the modal when the 'Know More' button is clicked
knowMoreButton.addEventListener('click', () => {
    modal.classList.add('show'); // Add class to show the modal with animation
    modal.classList.remove('fade-out'); // Remove fade-out class if modal is being shown
});

// Add event listener to close the modal when the close button is clicked
closeModal.addEventListener('click', () => {
    modal.classList.add('fade-out'); // Add fade-out class to trigger fade-out animation
    setTimeout(() => {
        modal.classList.remove('show', 'fade-out'); // Remove 'show' and 'fade-out' classes after animation
    }, 400); // Match the animation duration (e.g., 400ms)
});

// Add event listener to close the modal if the user clicks outside of it
window.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.classList.add('fade-out'); // Add fade-out class to trigger fade-out animation
        setTimeout(() => {
            modal.classList.remove('show', 'fade-out'); // Remove 'show' and 'fade-out' classes after animation
        }, 400); // Match the animation duration (e.g., 400ms)
    }
});
