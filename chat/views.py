from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from chat.forms import MessageForm
from chat.models import Chat


@login_required
def chat(request, identifier):
    chat = get_object_or_404(Chat, identifier=identifier)
    # Add verification for group chats that are someway private
    if chat.chat_type == Chat.PRIVATE and request.user not in chat.members.all():
        raise Http404()
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
    messages = chat.messages.all()[:30]  # Add dynamic load messages with htmx
    context = {
        "chat_messages": messages,
        "form": form,
        "chat": chat,
    }
    if chat.chat_type == Chat.PRIVATE:
        other_user = chat.members.exclude(id=request.user.id).first()
        context["other_user"] = other_user
    return render(request, "chat/chat.html", context)


@login_required
def chat_user(request, username):
    if request.user.username == username:
        return redirect("users:profile_self")
    user = get_object_or_404(User, username=username)
    chat = (
        Chat.objects.annotate(num_members=Count("members"))
        .filter(chat_type=Chat.PRIVATE, num_members=2, members=request.user)
        .filter(members=user)
        .first()
    )
    if not chat:
        chat = Chat.objects.create(chat_type=Chat.PRIVATE)
        chat.members.add(request.user, user)
    return redirect("chat:chat", identifier=chat.identifier)
