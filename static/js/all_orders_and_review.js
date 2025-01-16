document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chatMessages');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendMessage');
    const stars = document.querySelectorAll('.rating i');
    const feedbackForm = document.getElementById('feedbackForm');
    let selectedRating = 0;

    // Add welcome message
    addMessage("Welcome to Foodify! How can we help you today?", 'received');

    // Send message function
    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            addMessage(message, 'sent');
            messageInput.value = '';

            // Simulate auto-response
            setTimeout(() => {
                const responses = [
                    "Thank you for your message. Our team will get back to you shortly.",
                    "We've received your message and will respond as soon as possible.",
                    "Thanks for reaching out! We'll handle your request promptly."
                ];
                const randomResponse = responses[Math.floor(Math.random() * responses.length)];
                addMessage(randomResponse, 'received');
            }, 1000);
        }
    }

    // Add message to chat
    function addMessage(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Handle star rating
    stars.forEach(star => {
        star.addEventListener('click', () => {
            selectedRating = star.dataset.rating;
            stars.forEach(s => {
                if (s.dataset.rating <= selectedRating) {
                    s.classList.add('active');
                } else {
                    s.classList.remove('active');
                }
            });
        });
    });

    // Handle form submission
    feedbackForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const restaurant = document.getElementById('feedbackType').value;
        const feedback = document.getElementById('feedbackText').value;

        if (!selectedRating || !restaurant || !feedback) {
            alert('Please fill in all fields and select a rating');
            return;
        }

        try {
            const response = await fetch('/api/v1/submit_review', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    restaurant,
                    rating: selectedRating,
                    feedback
                })
            });

            const data = await response.json();
            if (data.success) {
                alert('Thank you for your feedback!');
                feedbackForm.reset();
                stars.forEach(s => s.classList.remove('active'));
                selectedRating = 0;
            } else {
                alert(data.error || 'Error submitting review');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error submitting review');
        }
    });
});
