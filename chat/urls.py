from django.urls import path

from chat import views

app_name = "chat"

urlpatterns = [
    path("users/@<str:username>/", views.chat_user, name="chat_user"),
    path("<str:identifier>/", views.chat, name="chat"),
]
