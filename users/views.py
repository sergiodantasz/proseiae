from allauth.account.views import PasswordChangeView as AllauthPasswordChangeView
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from users.forms import DeleteAccountForm, UserProfileForm
from utils.users import set_admin_user


@login_required
def profile(request, username=None):
    user = request.user if not username else get_object_or_404(User, username=username)
    ### REMOVE IT ###
    set_admin_user(user.username)
    #################
    profile = user.profile
    if username and user == request.user:
        return redirect("users:profile_self")
    return render(request, "account/profile.html", {"profile": profile})


@login_required
def settings(request):
    return render(request, "account/settings.html")


@login_required
def delete(request):
    form = DeleteAccountForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Sua conta foi excluída com sucesso.")
        return redirect("account_login")
    return render(request, "account/delete.html", {"form": form})


@login_required
def profile_edit(request):
    profile = request.user.profile
    form = UserProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=profile,
        user=request.user,
    )
    if request.method == "POST" and form.is_valid():
        avatar_action = form.cleaned_data.get("avatar_action")
        if avatar_action == "remove" and profile.avatar:
            profile.avatar.delete(save=False)
            profile.avatar = None
            profile.save()
        form.save()
        messages.success(request, "Seu perfil foi atualizado com sucesso.")
        return redirect("users:profile_self")
    return render(request, "account/profile_edit.html", {"form": form})


class PasswordChangeView(AllauthPasswordChangeView):
    success_url = reverse_lazy("users:profile_self")
