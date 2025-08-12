function scrollToBottom() {
  const messagesContainer = document.getElementById("messages_container");
  if (messagesContainer) {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }
}

scrollToBottom();

const form = document.getElementById("message_form");

if (form) {
  form.addEventListener("htmx:wsAfterSend", function () {
    this.reset();
  });
}

document.body.addEventListener("htmx:wsAfterMessage", (e) => {
  const message = e.detail.message || "";
  if (message.includes('id="messages_container"')) {
    const emptyChatAlert = document.getElementById("empty_chat_alert");
    if (emptyChatAlert) {
      emptyChatAlert.remove();
    }
    scrollToBottom();
  }
});
