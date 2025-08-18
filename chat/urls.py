from django.urls import path

from chat import views

app_name = "chat"

urlpatterns = [
    path("users/@<str:username>/", views.chat_user, name="chat_user"),
    path("create/", views.chat_create, name="chat_create"),
    path("home/", views.chat_home, name="chat_home"),
    path("<str:identifier>/", views.chat, name="chat"),
    path("edit/<str:identifier>/", views.chat_edit, name="chat_edit"),
    path("delete/<str:identifier>/", views.chat_delete, name="chat_delete"),
    path("leave/<str:identifier>/", views.chat_leave, name="chat_leave"),
]
