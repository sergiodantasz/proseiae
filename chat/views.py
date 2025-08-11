from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from chat.forms import MessageForm
from chat.models import Chat


@login_required
def chat(request):
    chat = get_object_or_404(Chat, identifier="public")  # Change it
    form = MessageForm(request.POST or None)
    if request.method == "POST" and request.htmx and form.is_valid():
        message = form.save(commit=False)
        message.sender = request.user
        message.chat = chat
        message.save()
        return render(
            request,
            "chat/partials/_message.html",
            {"message": message, "user": request.user},
        )
    messages = chat.messages.all()[:30]
    return render(
        request,
        "chat/chat.html",
        {"chat_messages": messages, "form": form},
    )
