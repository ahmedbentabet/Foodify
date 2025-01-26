/**
 * @file Contact form and feedback management
 */

/**
 * @typedef {Object} ReviewData
 * @property {string} restaurant_id
 * @property {number} rating
 * @property {string} feedback
 */

document.addEventListener("DOMContentLoaded", () => {
  const elements = {
    chatMessages: /** @type {HTMLElement} */ (
      document.getElementById("chatMessages")
    ),
    messageInput: /** @type {HTMLInputElement} */ (
      document.getElementById("messageInput")
    ),
    sendButton: /** @type {HTMLButtonElement} */ (
      document.getElementById("sendMessage")
    ),
    stars: /** @type {NodeListOf<HTMLElement>} */ (
      document.querySelectorAll(".rating i")
    ),
    feedbackForm: /** @type {HTMLFormElement} */ (
      document.getElementById("feedbackForm")
    ),
    ratingText: /** @type {HTMLElement} */ (
      document.querySelector(".rating-text")
    ),
  };

  let selectedRating = 0;

  const ratingTexts = {
    1: "Poor",
    2: "Fair",
    3: "Good",
    4: "Very Good",
    5: "Excellent",
  };

  /**
   * Adds a message to the chat display
   * @param {string} text - Message content
   * @param {'sent'|'received'} type - Message type
   */
  const addMessage = (text, type) => {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = text;
    elements.chatMessages.appendChild(messageDiv);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
  };

  // Initialize with welcome message
  addMessage("Welcome to Foodify! How can we help you today?", "received");

  // Send message function
  function sendMessage() {
    const message = elements.messageInput.value.trim();
    if (message) {
      addMessage(message, "sent");
      elements.messageInput.value = "";

      // Simulate auto-response
      setTimeout(() => {
        const responses = [
          "Thank you for your message. Our team will get back to you shortly.",
          "We've received your message and will respond as soon as possible.",
          "Thanks for reaching out! We'll handle your request promptly.",
        ];
        const randomResponse =
          responses[Math.floor(Math.random() * responses.length)];
        addMessage(randomResponse, "received");
      }, 1000);
    }
  }

  // Event listeners
  elements.sendButton.addEventListener("click", sendMessage);
  elements.messageInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // Handle star rating
  elements.stars.forEach((star) => {
    star.addEventListener("mouseenter", () => {
      const rating = parseInt(star.dataset.rating);
      highlightStars(rating);
      elements.ratingText.textContent = ratingTexts[rating];
    });

    star.addEventListener("mouseleave", () => {
      highlightStars(selectedRating);
      elements.ratingText.textContent = selectedRating
        ? ratingTexts[selectedRating]
        : "Select your rating";
    });

    star.addEventListener("click", () => {
      selectedRating = parseInt(star.dataset.rating);
      highlightStars(selectedRating);
      elements.ratingText.textContent = ratingTexts[selectedRating];
      elements.feedbackForm.querySelector(
        'button[type="submit"]'
      ).disabled = false;
    });
  });

  function highlightStars(rating) {
    elements.stars.forEach((s) => {
      const starRating = parseInt(s.dataset.rating);
      s.classList.toggle("active", starRating <= rating);
    });
  }

  // Handle form submission
  elements.feedbackForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const restaurantId = document.getElementById("feedbackType").value;
    const feedback = document.getElementById("feedbackText").value;

    try {
      const response = await fetch("/api/v1/submit_review", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          restaurant_id: restaurantId,
          rating: selectedRating,
          feedback,
        }),
      });

      const data = await response.json();

      if (data.success) {
        showSuccessMessage();
        resetForm();
      } else {
        alert(data.error || "Error submitting review");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error submitting review");
    }
  });

  function showSuccessMessage() {
    const successMessage = document.getElementById("successMessage");
    successMessage.style.display = "block";

    setTimeout(() => {
      successMessage.style.opacity = "0";
      setTimeout(() => {
        successMessage.style.display = "none";
        successMessage.style.opacity = "1";
      }, 500);
    }, 3000);
  }

  function resetForm() {
    elements.feedbackForm.reset();
    selectedRating = 0;
    highlightStars(0);
    elements.ratingText.textContent = "Select your rating";
    elements.feedbackForm.querySelector(
      'button[type="submit"]'
    ).disabled = true;
  }

  // Add cart count update functionality
  function updateCartCount() {
    const cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];
    const cartCount = document.getElementById("cart-count");
    const totalQuantity = cartItems.reduce(
      (total, item) => total + item.quantity,
      0
    );

    if (totalQuantity > 0) {
      cartCount.textContent = totalQuantity;
      cartCount.classList.remove("cart-count-hidden");
      cartCount.classList.add("cart-count-active");
    } else {
      cartCount.classList.remove("cart-count-active");
      cartCount.classList.add("cart-count-hidden");
    }
  }

  // Initialize cart count
  updateCartCount();
});
