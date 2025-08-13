from json import loads

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from chat.models import Chat, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.identifier = self.scope["url_route"]["kwargs"]["identifier"]
        self.chat = await self._get_object_or_404(Chat, identifier=self.identifier)
        await self.channel_layer.group_add(self.identifier, self.channel_name)
        online_users = await self._get_online_users()
        if self.user not in online_users:
            await sync_to_async(self.chat.online_users.add)(self.user)
            await self.update_online()
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.identifier, self.channel_name)
        online_users = await self._get_online_users()
        if self.user in online_users:
            await sync_to_async(self.chat.online_users.remove)(self.user)
            await self.update_online()

    async def receive(self, text_data):
        data = loads(text_data)
        content = data.get("content", "")
        message = await sync_to_async(Message.objects.create)(
            chat=self.chat, sender=self.user, content=content
        )
        event = {
            "type": "message_handler",
            "message_id": message.id,
        }
        await self.channel_layer.group_send(self.identifier, event)

    async def message_handler(self, event):
        message = await self._get_object_or_404(Message, id=event["message_id"])
        context = {
            "message": message,
            "user": self.user,
        }
        html = await self._render("chat/partials/_message-ws.html", context)
        await self.send(text_data=html)

    async def update_online(self):
        online_users_count = await sync_to_async(self.chat.online_users.count)()
        if self.chat.chat_type == "private":
            event = {
                "type": "online_user_status_handler",
                "is_user_online": online_users_count == 2,
            }
        else:
            event = {
                "type": "online_users_count_handler",
                "online_users_count": online_users_count,
            }
        await self.channel_layer.group_send(self.identifier, event)

    async def online_users_count_handler(self, event):
        context = {
            "online_users_count": event["online_users_count"],
        }
        html = await self._render("chat/partials/_online-users-count.html", context)
        await self.send(text_data=html)

    async def online_user_status_handler(self, event):
        context = {
            "is_user_online": event["is_user_online"],
        }
        html = await self._render("chat/partials/_online-user-status.html", context)
        await self.send(text_data=html)

    async def _render(self, template_name, context):
        return await sync_to_async(render_to_string)(template_name, context)

    async def _get_online_users(self):
        return await sync_to_async(list)(self.chat.online_users.all())

    async def _get_object_or_404(self, model, *args, **kwargs):
        return await sync_to_async(get_object_or_404)(model, *args, **kwargs)
