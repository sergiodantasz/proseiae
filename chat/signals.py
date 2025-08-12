from django.db.models.signals import post_migrate
from django.dispatch import receiver

from chat.models import Chat


@receiver(post_migrate)
def create_general_chat(sender, **kwargs):
    if sender.name == "chat":
        Chat.create_general_chat()
