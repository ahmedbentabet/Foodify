/**
 * @file Authentication and signup management
 */

document.addEventListener('DOMContentLoaded', () => {
    const elements = {
        loginBtn: /** @type {HTMLElement|null} */ (document.getElementById('loginBtn')),
        signUpBtn: /** @type {HTMLElement|null} */ (document.getElementById('signUpBtn')),
        flipCard: /** @type {HTMLElement|null} */ (document.querySelector('.flip-card__inner')),
        toggle: /** @type {HTMLInputElement|null} */ (document.getElementById('toggleSwitch'))
    };

    const urlParams = new URLSearchParams(window.location.search);
    const isSignupMode = urlParams.get('mode') === 'signup';

    // Initialize UI state
    if (elements.flipCard && elements.toggle) {
        elements.flipCard.style.transform = isSignupMode ? 'rotateY(180deg)' : 'rotateY(0deg)';
        elements.toggle.checked = isSignupMode;
    }

    // Event handlers
    const handleModeSwitch = (showSignup) => {
        if (elements.flipCard && elements.toggle) {
            elements.flipCard.style.transform = showSignup ? 'rotateY(180deg)' : 'rotateY(0deg)';
            elements.toggle.checked = showSignup;
        }
    };

    elements.signUpBtn?.addEventListener('click', () => handleModeSwitch(true));
    elements.loginBtn?.addEventListener('click', () => handleModeSwitch(false));
    elements.toggle?.addEventListener('change', (e) => {
        handleModeSwitch(/** @type {HTMLInputElement} */ (e.target).checked);
    });

    // Form validation
    const signUpForm = /** @type {HTMLFormElement|null} */ (document.getElementById('signUpForm'));
    signUpForm?.addEventListener('submit', (e) => {
        const password = /** @type {HTMLInputElement} */ (document.getElementById('password')).value;
        const passwordAgain = /** @type {HTMLInputElement} */ (document.getElementById('passwordAgain')).value;
        const errorMessage = /** @type {HTMLElement|null} */ (document.getElementById('error-message'));

        if (password !== passwordAgain) {
            e.preventDefault();
            if (errorMessage) errorMessage.style.display = 'block';
        } else if (errorMessage) {
            errorMessage.style.display = 'none';
        }
    });
});
