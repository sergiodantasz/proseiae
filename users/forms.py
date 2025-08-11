from allauth.account import forms as allauth_forms
from django import forms
from django.contrib.auth.models import User

from core.mixins import CssClassMixin, LabelMixin, PlaceholderMixin
from users.models import Profile


class LoginForm(CssClassMixin, PlaceholderMixin, LabelMixin, allauth_forms.LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_label("login", "E-mail")
        self.apply_css_classes()
        self.apply_placeholders()


class SignupForm(CssClassMixin, PlaceholderMixin, LabelMixin, allauth_forms.SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_label("email", "E-mail")
        self.apply_css_classes()
        self.apply_placeholders()

    def clean_username(self):
        username = super().clean_username()
        if username != username.lower():
            raise forms.ValidationError(
                "O nome de usuário deve conter apenas letras minúsculas.",
                code="invalid",
            )
        return username


class ResetPasswordForm(
    CssClassMixin, PlaceholderMixin, LabelMixin, allauth_forms.ResetPasswordForm
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_label("email", "E-mail")
        self.apply_css_classes()
        self.apply_placeholders()


class ResetPasswordKeyForm(
    CssClassMixin, PlaceholderMixin, LabelMixin, allauth_forms.ResetPasswordKeyForm
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_label("password1", "Nova senha")
        self.set_label("password2", "Confirme a nova senha")
        self.apply_css_classes()
        self.apply_placeholders()


class DeleteAccountForm(CssClassMixin, forms.Form):
    confirm_delete = forms.BooleanField(
        label="Sim, desejo excluir minha conta e entendo que esta ação é irreversível.",
        required=True,
        error_messages={
            "required": "Você precisa confirmar que deseja excluir sua conta.",
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_css_classes()


class ChangePasswordForm(
    CssClassMixin, PlaceholderMixin, LabelMixin, allauth_forms.ChangePasswordForm
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_label("oldpassword", "Senha atual")
        self.set_label("password1", "Nova senha")
        self.set_label("password2", "Confirme a nova senha")
        self.apply_css_classes()
        self.apply_placeholders()


class AddEmailForm(
    CssClassMixin, PlaceholderMixin, LabelMixin, allauth_forms.AddEmailForm
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_label("email", "E-mail")
        self.apply_css_classes()
        self.apply_placeholders()


class UserProfileForm(CssClassMixin, PlaceholderMixin, LabelMixin, forms.ModelForm):
    avatar_action = forms.ChoiceField(
        choices=[("keep", "Manter"), ("remove", "Remover")],
        widget=forms.RadioSelect,
        initial="keep",
    )
    first_name = forms.CharField(required=False, label="Primeiro nome")
    last_name = forms.CharField(required=False, label="Último nome")
    username = forms.CharField(required=True, label="Nome de usuário")

    class Meta:
        model = Profile
        fields = [
            "avatar_action",
            "avatar",
            "first_name",
            "last_name",
            "username",
            "bio",
        ]
        widgets = {"avatar": forms.FileInput()}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user := self.user:
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            self.fields["username"].initial = user.username
        self.set_label("avatar", "Avatar")
        self.set_label("bio", "Bio")
        self.apply_css_classes()
        self.apply_placeholders()

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.exclude(pk=self.user.pk).filter(username=username).exists():
            raise forms.ValidationError(
                User._meta.get_field("username").error_messages["unique"],
                code="unique",
            )
        if username != username.lower():
            raise forms.ValidationError(
                "O nome de usuário deve conter apenas letras minúsculas.",
                code="invalid",
            )
        return username

    def save(self, commit=True):
        profile = super().save(commit=False)
        if user := self.user:
            user.first_name = self.cleaned_data.get("first_name", user.first_name)
            user.last_name = self.cleaned_data.get("last_name", user.last_name)
            user.username = self.cleaned_data.get("username", user.username)
            if commit:
                user.save()
        if commit:
            profile.save()
        return profile
