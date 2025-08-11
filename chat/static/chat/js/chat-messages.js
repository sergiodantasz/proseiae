function scrollToBottom() {
  const container = document.getElementById("messages_container");
  if (container) {
    container.scrollTop = container.scrollHeight;
  }
}

scrollToBottom();

const form = document.getElementById("message_form");

if (form) {
  form.addEventListener("htmx:beforeSend", function () {
    this.reset();
  });
}

document.body.addEventListener("htmx:afterSwap", (e) => {
  if (e.detail.target.id === "messages_container") {
    const emptyChatAlert = document.getElementById("empty_chat_alert");
    if (emptyChatAlert) {
      emptyChatAlert.remove();
    }
    scrollToBottom();
  }
});
