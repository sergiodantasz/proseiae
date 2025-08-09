setTimeout(() => {
  const messageContainer = document.getElementById("message-container");
  if (messageContainer) {
    messageContainer.classList.remove(
      "animate-in",
      "fade-in",
      "zoom-in",
      "slide-in-from-bottom"
    );
    messageContainer.classList.add(
      "animate-out",
      "fade-out",
      "zoom-out",
      "slide-out-to-bottom"
    );
    setTimeout(() => {
      messageContainer.remove();
    }, 150);
  }
}, 5000);
