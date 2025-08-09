from django import forms


class CssClassMixin:
    WIDGET_CLASSES = {
        forms.CheckboxInput: "checkbox checkbox-sm",
        forms.PasswordInput: "input w-full",
        forms.EmailInput: "input w-full",
        forms.TextInput: "input w-full",
        forms.FileInput: "file-input w-full",
        forms.Textarea: "textarea w-full",
        forms.RadioSelect: "radio radio-sm",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_css_classes()

    def set_css_class(self, field_name: str, *css_classes):
        field = self.fields.get(field_name)
        if not field:
            return
        existing_classes = field.widget.attrs.get("class", "")
        classes = set(existing_classes.split())
        for css_class in css_classes:
            classes.add(css_class)
        field.widget.attrs["class"] = " ".join(classes)

    def apply_css_classes(self):
        for field_name, field in self.fields.items():
            widget = field.widget
            css_class = "input"
            for widget_cls, class_str in self.WIDGET_CLASSES.items():
                if isinstance(widget, widget_cls):
                    css_class = class_str
                    break
            self.set_css_class(field_name, css_class)


class PlaceholderMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_placeholders()

    def set_placeholder(self, field_name: str, placeholder: str):
        field = self.fields.get(field_name)
        if field and "placeholder" not in field.widget.attrs:
            field.widget.attrs["placeholder"] = placeholder

    def apply_placeholders(self):
        for field_name, field in self.fields.items():
            if field.label:
                self.set_placeholder(field_name, field.label)


class LabelMixin:
    def set_label(self, field_name: str, label: str):
        field = self.fields.get(field_name)
        if field:
            field.label = label
