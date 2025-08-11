from django import template

register = template.Library()


@register.simple_tag
def avatar_url(user, size=64, theme="emerald"):
    return user.profile.get_avatar_url(size, theme)
