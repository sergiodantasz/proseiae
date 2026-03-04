from django.urls import path

from chat.consumers import ChatConsumer, ChatHomeConsumer

websocket_urlpatterns = [
    path("ws/chat/<str:identifier>/", ChatConsumer.as_asgi()),
    path("ws/home/", ChatHomeConsumer.as_asgi()),
]
