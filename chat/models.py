from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    identifier = models.CharField(
        max_length=128,
        unique=True,
        default=uuid4,
    )
    name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
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
    is_private = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.name or str(self.identifier)


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
