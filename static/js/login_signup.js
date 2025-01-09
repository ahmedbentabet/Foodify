document.addEventListener("DOMContentLoaded", function () {
    const loginBtn = document.getElementById("loginBtn");
    const signUpBtn = document.getElementById("signUpBtn");
    const flipCardInner = document.querySelector(".flip-card__inner");
    const toggleSwitch = document.getElementById("toggleSwitch");

    // Read URL parameters to determine the default mode
    const urlParams = new URLSearchParams(window.location.search);
    const mode = urlParams.get("mode"); // Read the "mode" value

    // Set the default state based on the "mode" value
    if (mode === "signup") {
        flipCardInner.style.transform = "rotateY(180deg)"; // Show the Sign-Up page
        toggleSwitch.checked = true; // Activate the toggle switch
    } else {
        flipCardInner.style.transform = "rotateY(0deg)"; // Show the Login page
        toggleSwitch.checked = false; // Deactivate the toggle switch
    }

    // When clicking the "Sign Up" button
    signUpBtn.addEventListener("click", function () {
        flipCardInner.style.transform = "rotateY(180deg)"; // Flip the card to show the Sign-Up page
        toggleSwitch.checked = true; // Activate the toggle switch when clicking "Sign Up"
    });

    // When clicking the "Login" button
    loginBtn.addEventListener("click", function () {
        flipCardInner.style.transform = "rotateY(0deg)"; // Flip the card back to the Login page
        toggleSwitch.checked = false; // Deactivate the toggle switch when clicking "Login"
    });

    // When clicking the toggle switch itself
    toggleSwitch.addEventListener("change", function () {
        if (toggleSwitch.checked) {
            flipCardInner.style.transform = "rotateY(180deg)"; // Flip the card to the Sign-Up page
        } else {
            flipCardInner.style.transform = "rotateY(0deg)"; // Flip the card back to the Login page
        }
    });
});

document.getElementById("signUpForm").addEventListener("submit", function (event) {
    var password = document.getElementById("password").value;
    var passwordAgain = document.getElementById("passwordAgain").value;
    var errorMessage = document.getElementById("error-message");

    if (password !== passwordAgain) {
        event.preventDefault(); // Prevent form submission if passwords do not match
        errorMessage.style.display = "block"; // Display error message
    } else {
        errorMessage.style.display = "none"; // Hide error message if passwords match
    }
});
