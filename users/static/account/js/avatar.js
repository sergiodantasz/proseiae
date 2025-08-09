document.addEventListener("DOMContentLoaded", () => {
  const avatarElement = document.getElementById("avatar");
  const avatarFileInput = document.getElementById("id_avatar");

  const profileForm = document.getElementById("user-profile-form");
  if (!profileForm) return;

  const avatarActionModal = document.getElementById("avatar_action_modal");
  const confirmAvatarAcationBtn = document.getElementById(
    "confirm-avatar-action-btn"
  );
  const cancelAvatarActionBtn = document.getElementById(
    "cancel-avatar-action-btn"
  );

  const userHasAvatar = profileForm.dataset.userHasAvatar === "true";

  if (avatarElement && avatarFileInput) {
    avatarElement.addEventListener("click", () => {
      avatarFileInput.click();
    });
  }

  if (avatarFileInput && avatarActionModal) {
    profileForm.addEventListener("submit", (e) => {
      if (userHasAvatar && avatarFileInput.files.length === 0) {
        e.preventDefault();
        avatarActionModal.showModal();
      }
    });
  }

  if (cancelAvatarActionBtn && avatarActionModal) {
    cancelAvatarActionBtn.addEventListener("click", () => {
      avatarActionModal.close();
    });
  }

  if (confirmAvatarAcationBtn && avatarActionModal) {
    confirmAvatarAcationBtn.addEventListener("click", () => {
      avatarActionModal.close();
      profileForm.submit();
    });
  }
});
