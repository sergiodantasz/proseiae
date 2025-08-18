from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from chat.forms import ChatForm, DeleteChatForm, MessageForm
from chat.models import Chat


@login_required
def chat_home(request):
    private_chats = request.user.chats_member.filter(chat_type=Chat.PRIVATE)
    group_chats = request.user.chats_member.filter(chat_type=Chat.GROUP)
    if request.method == "POST":
        username = request.POST.get("username")
        if username:
            if User.objects.filter(username=username).exists():
                return redirect("chat:chat_user", username=username)
            messages.error(request, "Usuário não encontrado.")
            return redirect("chat:chat_home")
        identifier = request.POST.get("identifier")
        if identifier:
            if Chat.objects.filter(
                chat_type=Chat.GROUP, identifier=identifier
            ).exists():
                return redirect("chat:chat", identifier=identifier)
            messages.error(request, "Chat não encontrado.")
            return redirect("chat:chat_home")
    return render(
        request,
        "chat/chat_home.html",
        {"private_chats": private_chats, "group_chats": group_chats},
    )


@login_required
def chat(request, identifier):
    chat = get_object_or_404(Chat, identifier=identifier)
    # What if the user change the e-mail and it is not verified, but he already was a member?
    # TODO: Verify if the user whose the current user is trying to access the chat has been verified his email
    if (
        chat.chat_type != Chat.GENERAL
        and not request.user.emailaddress_set.first().verified
    ):
        messages.error(
            request, "Você precisa verificar seu e-mail para entrar no chat."
        )
        return redirect("home:home")
    if chat.chat_type == Chat.PRIVATE and request.user not in chat.members.all():
        raise Http404()
    if chat.chat_type == Chat.GROUP:
        # TODO: Add group chat privacy settings
        if request.user not in chat.members.all():
            chat.members.add(request.user)
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
    chat_messages = chat.messages.all()[:30]  # Add dynamic load messages with htmx
    context = {
        "chat_messages": chat_messages,
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
    if not request.user.emailaddress_set.first().verified:
        messages.error(
            request, "Você precisa verificar seu e-mail para poder criar um chat."
        )
        return redirect("chat:chat_home")
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


@login_required
def chat_create(request):
    if not request.user.emailaddress_set.first().verified:
        messages.error(
            request, "Você precisa verificar seu e-mail para poder criar um chat."
        )
        return redirect("home:home")
    form = ChatForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        chat = form.save(commit=False)
        chat.owner = request.user
        chat.chat_type = Chat.GROUP
        chat.save()
        chat.members.add(request.user)
        messages.success(request, "Chat criado com sucesso.")
        return redirect("chat:chat", identifier=chat.identifier)
    return render(request, "chat/chat_create.html", {"form": form})


@login_required
def chat_edit(request, identifier):
    chat = get_object_or_404(Chat, identifier=identifier)
    if chat.owner != request.user:
        raise Http404()
    form = ChatForm(request.POST or None, instance=chat, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        members_to_keep = [
            get_object_or_404(User, username=username)
            for username in request.POST.getlist("keep_member")
        ]
        for member in chat.members.all():
            if member not in members_to_keep:
                chat.members.remove(member)
        messages.success(request, "Chat atualizado com sucesso.")
        return redirect("chat:chat", identifier=chat.identifier)
    return render(request, "chat/chat_edit.html", {"form": form, "chat": chat})


@login_required
def chat_delete(request, identifier):
    chat = get_object_or_404(Chat, identifier=identifier)
    if chat.owner != request.user:
        raise Http404()
    form = DeleteChatForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        chat.delete()
        messages.success(request, "Chat deletado com sucesso.")
        return redirect("home:home")
    return render(request, "chat/chat_delete.html", {"form": form, "chat": chat})


# TODO: Block user from leave chat if he is the owner of the chat
# TODO: Block user from leave chat if the chat is the general chat
@login_required
def chat_leave(request, identifier):
    chat = get_object_or_404(Chat, identifier=identifier)
    if (
        not request.method == "POST"
        or chat.chat_type != Chat.GROUP
        or request.user not in chat.members.all()
    ):
        raise Http404()
    chat.members.remove(request.user)
    messages.success(request, "Você saiu do chat com sucesso.")
    return redirect("home:home")
