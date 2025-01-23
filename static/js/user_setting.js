/**
 * @file User profile settings management
 */

document.addEventListener("DOMContentLoaded", () => {
  const elements = {
    profileForm: /** @type {HTMLFormElement|null} */ (
      document.getElementById("profileForm")
    ),
    photoUpload: /** @type {HTMLInputElement|null} */ (
      document.getElementById("photoUpload")
    ),
    userPhoto: /** @type {HTMLImageElement|null} */ (
      document.getElementById("userPhoto")
    ),
  };

  // Handle photo upload
  elements.photoUpload?.addEventListener("change", (e) => {
    const target = /** @type {HTMLInputElement} */ (e.target);
    const file = target.files?.[0];

    if (file && elements.userPhoto) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const result = /** @type {string} */ (e.target?.result);
        if (elements.userPhoto && result) {
          elements.userPhoto.src = result;
          localStorage.setItem("userPhoto", result);
        }
      };
      reader.readAsDataURL(file);
    }
  });

  // Handle form submission
  elements.profileForm?.addEventListener("submit", (e) => {
    e.preventDefault();

    const formData = {
      username: /** @type {HTMLInputElement} */ (
        document.getElementById("username")
      ).value,
      email: /** @type {HTMLInputElement} */ (document.getElementById("email"))
        .value,
      oldPassword: /** @type {HTMLInputElement} */ (
        document.getElementById("oldPassword")
      ).value,
      newPassword: /** @type {HTMLInputElement} */ (
        document.getElementById("newPassword")
      ).value,
      confirmPassword: /** @type {HTMLInputElement} */ (
        document.getElementById("confirmPassword")
      ).value,
    };

    if (formData.newPassword !== formData.confirmPassword) {
      alert("New passwords don't match!");
      return;
    }

    // TODO: Add API call to update user profile
    alert("Profile updated successfully!");
  });

  // Load saved photo if exists
  const savedPhoto = localStorage.getItem("userPhoto");
  if (savedPhoto && elements.userPhoto) {
    elements.userPhoto.src = savedPhoto;
  }
});
