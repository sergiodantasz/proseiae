from allauth.account.views import PasswordChangeView as AllauthPasswordChangeView
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import uri_to_iri

from users.forms import DeleteAccountForm, UserProfileForm


@login_required
def profile(request, username=None):
    # if request.user.username == "sergio":
    #     userr = get_object_or_404(User, username=request.user.username)
    #     userr.is_staff = True
    #     userr.is_superuser = True
    #     userr.save()
    user_ = request.user if not username else get_object_or_404(User, username=username)
    if username and user_ == request.user:
        return redirect("users:profile_self")
    return render(request, "account/profile.html", {"user_": user_})


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


@login_required
def avatar_partial(request):
    if request.headers.get("HX-Request") != "true":
        raise Http404()
    avatar_size = request.GET.get("avatar_size", 64)
    try:
        avatar_size = int(avatar_size)
    except (ValueError, TypeError):
        avatar_size = 64
    extra_classes = request.GET.get("extra_classes", "")
    extra_attrs = uri_to_iri(request.GET.get("extra_attrs", ""))
    return render(
        request,
        "account/partials/_avatar.html",
        {
            "request_user": request.user,
            "avatar_size": avatar_size,
            "extra_classes": extra_classes,
            "extra_attrs": extra_attrs,
        },
    )
