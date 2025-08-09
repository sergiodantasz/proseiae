from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("profile/<str:username>/", views.profile, name="profile_detail"),
    path("profile/", views.profile, name="profile_self"),
    path("settings/", views.settings, name="settings"),
    path("delete/", views.delete, name="delete"),
    path(
        "password/change/",
        views.PasswordChangeView.as_view(),
        name="account_change_password",
    ),
]
