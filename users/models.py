from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def name(self):
        return self.user.get_full_name().strip() or self.user.username

    def get_avatar_url(self, size, theme="emerald"):
        if self.avatar:
            return self.avatar.url
        theme_colors = {
            "emerald": ("66cc8a", "223d30"),
            "night": ("3abdf8", "010d15"),
        }
        bg, color = theme_colors.get(theme, theme_colors["emerald"])
        return f"https://ui-avatars.com/api/?background={bg}&color={color}&size={size}&name={self.name}"
