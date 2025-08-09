from django import template
from django.contrib.messages import constants
from django.utils.safestring import mark_safe
from heroicons.templatetags.heroicons import heroicon_outline

register = template.Library()

ICON_NAMES = {
    constants.SUCCESS: "check-circle",
    constants.ERROR: "x-circle",
    constants.WARNING: "exclamation-circle",
    constants.INFO: "information-circle",
}


@register.simple_tag
def message_icon(level):
    icon_name = ICON_NAMES.get(level, "")
    if not icon_name:
        return mark_safe(f"<!-- Icon not found for message level: {level} -->")
    return heroicon_outline(icon_name)
