from json import loads

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from chat.models import Chat, Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.identifier = self.scope["url_route"]["kwargs"]["identifier"]
        self.chat = get_object_or_404(Chat, identifier=self.identifier)
        async_to_sync(self.channel_layer.group_add)(self.identifier, self.channel_name)
        if self.user not in self.chat.online_users.all():
            self.chat.online_users.add(self.user)
            self.update_online_users_count()
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.identifier, self.channel_name
        )
        if self.user in self.chat.online_users.all():
            self.chat.online_users.remove(self.user)
            self.update_online_users_count()

    def receive(self, text_data):
        text_data_json = loads(text_data)
        content = text_data_json.get("content", "")
        message = Message.objects.create(
            chat=self.chat,
            sender=self.user,
            content=content,
        )
        event = {
            "type": "message_handler",
            "message_id": message.id,
        }
        async_to_sync(self.channel_layer.group_send)(self.identifier, event)

    def message_handler(self, event):
        message_id = event["message_id"]
        message = get_object_or_404(Message, id=message_id)
        context = {
            "message": message,
            "user": self.user,
        }
        html = render_to_string("chat/partials/_message-ws.html", context)
        self.send(text_data=html)

    def update_online_users_count(self):
        online_users_count = self.chat.online_users.count()
        event = {
            "type": "online_users_count_handler",
            "online_users_count": online_users_count,
        }
        async_to_sync(self.channel_layer.group_send)(self.identifier, event)

    def online_users_count_handler(self, event):
        online_users_count = event["online_users_count"]
        context = {
            "online_users_count": online_users_count,
        }
        html = render_to_string("chat/partials/_online-users-count.html", context)
        self.send(text_data=html)
