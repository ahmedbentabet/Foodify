/**
 * @file Order management and cart functionality
 */

/** @type {HTMLElement|null} */
const orderItems = document.getElementById("orderItems");
/** @type {HTMLElement|null} */
const itemizedPrices = document.getElementById("itemizedPrices");
/** @type {HTMLElement|null} */
const subtotalElement = document.getElementById("subtotal");
/** @type {HTMLElement|null} */
const totalElement = document.getElementById("total");
/** @type {HTMLButtonElement|null} */
const proceedBtn = document.getElementById("proceedToDelivery");

const DELIVERY_FEE = 5.0;

/**
 * Updates the order summary display with current cart items
 * @returns {void}
 */
const updateOrderSummary = () => {
  if (
    !orderItems ||
    !itemizedPrices ||
    !subtotalElement ||
    !totalElement ||
    !proceedBtn
  ) {
    return;
  }

  orderItems.innerHTML = "";
  itemizedPrices.innerHTML = "";
  let subtotal = 0;

  cartItems.forEach((item) => {
    const { id, name, price, quantity, image = "default-meal.jpg" } = item;
    const itemTotal = price * quantity;

    // Create order item box
    const orderItem = document.createElement("div");
    orderItem.className = "order-item";
    orderItem.innerHTML = `
      <img src="${image}" alt="${name}">
      <div class="item-details">
        <h3>${name}</h3>
        <div class="item-controls">
          <div class="quantity-controls">
            <button class="quantity-btn decrease" data-id="${id}">-</button>
            <span class="quantity">${quantity}</span>
            <button class="quantity-btn increase" data-id="${id}">+</button>
          </div>
          <button class="remove-btn" data-id="${id}">Remove</button>
        </div>
      </div>
      <div class="item-price">$${itemTotal.toFixed(2)}</div>
    `;
    orderItems.appendChild(orderItem);

    // Add to itemized prices
    const itemPrice = document.createElement("div");
    itemPrice.className = "itemized-price";
    itemPrice.innerHTML = `
      <span>${name} x${quantity}</span>
      <span>$${itemTotal.toFixed(2)}</span>
    `;
    itemizedPrices.appendChild(itemPrice);

    subtotal += itemTotal;
  });

  subtotalElement.textContent = `$${subtotal.toFixed(2)}`;
  totalElement.textContent = `$${(subtotal + DELIVERY_FEE).toFixed(2)}`;
  proceedBtn.disabled = cartItems.length === 0;
};

// Event delegation for quantity controls
orderItems?.addEventListener("click", (e) => {
  const target = /** @type {HTMLElement} */ (e.target);
  if (target.classList.contains("quantity-btn")) {
    const itemId = target.dataset.id;
    const isIncrease = target.classList.contains("increase");
    updateItemQuantity(itemId, isIncrease);
    updateOrderSummary();
  }
});

updateOrderSummary();

document.getElementById("proceedToDelivery")?.addEventListener("click", () => {
  // Check if cart has items
  const cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];

  if (cartItems.length === 0) {
    alert("Your cart is empty! Please add items before proceeding.");
    return;
  }

  // Store order summary
  const orderSummary = {
    items: cartItems,
    subtotal: document.getElementById("subtotal")?.textContent,
    total: document.getElementById("total")?.textContent,
    deliveryFee: "5.00",
  };
  localStorage.setItem("orderSummary", JSON.stringify(orderSummary));

  // Navigate to delivery page
  window.location.href = "/delivery"; // Changed from /location
});
