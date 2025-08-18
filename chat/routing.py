from django.urls import path

from chat.consumers import ChatConsumer, ChatHomeConsumer, GlobalOnlineConsumer

websocket_urlpatterns = [
    path("ws/chat/<str:identifier>/", ChatConsumer.as_asgi()),
    path("ws/home/", ChatHomeConsumer.as_asgi()),
    path("ws/online/", GlobalOnlineConsumer.as_asgi()),
]
