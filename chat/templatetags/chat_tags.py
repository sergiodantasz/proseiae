from django import template

register = template.Library()


@register.filter
def other_user(chat, current_user):
    if chat.chat_type != chat.PRIVATE:
        return None
    return chat.members.exclude(id=current_user.id).first()
