from django import forms

from chat.models import Chat, Message
from core.mixins import (
    CssClassMixin,
    LabelMixin,
    PlaceholderMixin,
    SimpleWidgetAttrsMixin,
)


class MessageForm(
    CssClassMixin, PlaceholderMixin, LabelMixin, SimpleWidgetAttrsMixin, forms.ModelForm
):
    class Meta:
        model = Message
        fields = ["content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_label("content", "Digite uma mensagem...")
        self.set_widget_attrs({"content": {"autofocus": True}})
        self.apply_css_classes()
        self.apply_placeholders()


class ChatForm(
    CssClassMixin, PlaceholderMixin, LabelMixin, SimpleWidgetAttrsMixin, forms.ModelForm
):
    class Meta:
        model = Chat
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.set_label("name", "Nome do chat")
        self.apply_css_classes()
        self.apply_placeholders()

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if self.user:
            qs = Chat.objects.filter(owner=self.user, name=name)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Você já possui um chat com esse nome.")
        return name


class DeleteChatForm(CssClassMixin, forms.Form):
    confirm_delete = forms.BooleanField(
        label="Sim, desejo excluir o chat e entendo que esta ação é irreversível.",
        required=True,
        error_messages={
            "required": "Você precisa confirmar que deseja excluir o chat.",
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_css_classes()
