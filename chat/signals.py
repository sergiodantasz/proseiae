from django.contrib.auth.models import User
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from chat.models import Chat


@receiver(post_migrate)
def create_general_chat(sender, **kwargs):
    if sender.name == "chat":
        Chat.create_general_chat()


@receiver(post_save, sender=User)
def add_user_to_general_chat(sender, instance, created, **kwargs):
    if created:
        general_chat = Chat.objects.get(chat_type=Chat.GENERAL)
        general_chat.members.add(instance)
