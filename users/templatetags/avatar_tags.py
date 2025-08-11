from django import template

register = template.Library()


@register.simple_tag
def avatar_url(user, size):
    return user.profile.get_avatar_url(size)
