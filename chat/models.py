from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    GENERAL = "general"
    GROUP = "group"
    PRIVATE = "private"

    CHAT_TYPE_CHOICES = [
        (GENERAL, "Geral"),
        (GROUP, "Grupo"),
        (PRIVATE, "Privado"),
    ]

    identifier = models.CharField(
        max_length=128,
        unique=True,
        default=uuid4,
    )
    name = models.CharField(
        max_length=50,
        blank=True,
        default="",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="owned_chats",
        null=True,
    )
    online_users = models.ManyToManyField(
        User,
        related_name="chats_online",
        blank=True,
    )
    members = models.ManyToManyField(
        User,
        related_name="chats_member",
        blank=True,
    )
    chat_type = models.CharField(
        max_length=10,
        choices=CHAT_TYPE_CHOICES,
        default=GROUP,
    )

    def __str__(self):
        return self.name or f"Chat {self.identifier}"

    @classmethod
    def create_general_chat(cls):
        if not cls.objects.filter(identifier=cls.GENERAL).exists():
            cls.objects.create(
                identifier=cls.GENERAL,
                name="Chat Geral",
                chat_type=cls.GENERAL,
            )


class Message(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages_sent",
    )
    content = models.CharField(
        max_length=500,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"{self.sender.username}: {self.content}"
            if self.content
            else "Empty message"
        )
