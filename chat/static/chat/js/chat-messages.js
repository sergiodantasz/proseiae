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

document.body.addEventListener("htmx:afterSwap", function (e) {
  if (e.detail.target.id === "messages_container") {
    scrollToBottom();
  }
});
