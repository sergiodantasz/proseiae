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
