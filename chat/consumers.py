from json import loads

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from chat.models import Chat, Message


class BaseConsumer(AsyncWebsocketConsumer):
    async def render_template(self, template_name, context):
        return await sync_to_async(render_to_string)(template_name, context)

    async def send_template(self, template_name, context):
        html = await self.render_template(template_name, context)
        await self.send(text_data=html)

    @database_sync_to_async
    def fetch_object_or_404(self, model, *args, **kwargs):
        return get_object_or_404(model, *args, **kwargs)

    @database_sync_to_async
    def fetch_users_by_ids(self, ids):
        return User.objects.filter(id__in=ids)


class ChatConsumer(BaseConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_identifier = self.scope["url_route"]["kwargs"]["identifier"]
        self.chat = await self.fetch_object_or_404(
            Chat, identifier=self.room_identifier
        )
        await self.channel_layer.group_add(self.room_identifier, self.channel_name)
        await self._set_user_online()
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_identifier, self.channel_name)
        await self._set_user_offline()

    async def receive(self, text_data):
        data = loads(text_data)
        content = data.get("content", "")
        message = await self._create_message(content)
        await self.channel_layer.group_send(
            self.room_identifier,
            {
                "type": "on_message",
                "message_id": message.id,
            },
        )

    async def on_message(self, event):
        message = await self.fetch_object_or_404(Message, id=event["message_id"])
        await self.send_template(
            "chat/partials/_message-ws.html",
            {"message": message, "current_user": self.user},
        )

    async def _broadcast_chat_status(self):
        count = await self._count_online_users()
        event_type, payload = (
            ("on_private_chat_status", {"peer_online": count == 2})
            if self.chat.chat_type == "private"
            else ("on_group_online_count", {"online_count": count})
        )
        await self.channel_layer.group_send(
            self.room_identifier, {"type": event_type, **payload}
        )

    async def on_group_online_count(self, event):
        await self.send_template(
            "chat/partials/_chat-online-count.html",
            {
                "online_count": event["online_count"],
                "chat": self.chat,
            },
        )

    async def on_private_chat_status(self, event):
        await self.send_template(
            "chat/partials/_chat-private-status.html",
            {
                "peer_online": event["peer_online"],
            },
        )

    @database_sync_to_async
    def _is_user_online(self):
        return self.chat.online_users.filter(id=self.user.id).exists()

    @database_sync_to_async
    def _count_online_users(self):
        return self.chat.online_users.count()

    @database_sync_to_async
    def _add_online_user(self):
        self.chat.online_users.add(self.user)

    @database_sync_to_async
    def _remove_online_user(self):
        self.chat.online_users.remove(self.user)

    @database_sync_to_async
    def _create_message(self, content):
        return Message.objects.create(chat=self.chat, sender=self.user, content=content)

    async def _set_user_online(self):
        if not await self._is_user_online():
            await self._add_online_user()
            await self._broadcast_chat_status()
            await self._notify_home()

    async def _set_user_offline(self):
        if await self._is_user_online():
            await self._remove_online_user()
            await self._broadcast_chat_status()
            await self._notify_home()

    async def _notify_home(self):
        await self.channel_layer.group_send(
            "chat_home",
            {"type": "on_chat_home_update"},
        )


class GlobalOnlineConsumer(BaseConsumer):
    TTL = 30

    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = "global_online"
        self.redis = cache.client.get_client()
        await self._set_user_online()
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self._broadcast_online_users()

    async def receive(self, text_data):
        data = loads(text_data)
        if data.get("type") == "heartbeat" and self.user.is_authenticated:
            await self._set_or_refresh_ttl()

    async def disconnect(self, close_code):
        await self._set_user_offline()
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self._broadcast_online_users()

    async def on_global_status(self, event):
        # users = await self.fetch_users_by_ids(event["ids"])
        await self.send_template(
            "chat/partials/_global-online-users.html",
            {
                "global_online_count": len(event["ids"]),
            },
        )

    async def _set_or_refresh_ttl(self):
        await sync_to_async(self.redis.setex)(
            f"user:{self.user.id}:online", self.TTL, 1
        )

    async def _set_user_online(self):
        if self.user.is_authenticated:
            await self._set_or_refresh_ttl()

    async def _set_user_offline(self):
        if self.user.is_authenticated:
            await sync_to_async(self.redis.delete)(f"user:{self.user.id}:online")

    async def _get_online_user_ids(self):
        keys = await sync_to_async(self.redis.keys)("user:*:online")
        ids = [int(k.decode().split(":")[1]) for k in keys]
        return ids

    async def _broadcast_online_users(self):
        ids = await self._get_online_user_ids()
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "on_global_status",
                "ids": ids,
            },
        )


class ChatHomeConsumer(BaseConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = "chat_home"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.on_chat_home_update()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def on_chat_home_update(self, event=None):
        private_chats = await database_sync_to_async(self.user.chats_member.filter)(
            chat_type=Chat.PRIVATE
        )
        group_chats = await database_sync_to_async(self.user.chats_member.filter)(
            chat_type=Chat.GROUP
        )
        general_online_count = await self.get_general_online_count()
        await self.send_template(
            "chat/partials/_chat-home-update.html",
            {
                "private_chats": private_chats,
                "group_chats": group_chats,
                "general_online_count": general_online_count,
                "current_user": self.user,
            },
        )

    @staticmethod
    @database_sync_to_async
    def get_general_online_count():
        return Chat.objects.filter(chat_type=Chat.GENERAL).first().online_users.count()
