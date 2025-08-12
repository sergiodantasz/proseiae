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

    def get_avatar_url(self, size):
        if self.avatar:
            return self.avatar.url
        background_color = "3abdf8"
        color = "010d15"
        return f"https://ui-avatars.com/api/?background={background_color}&color={color}&size={size}&name={self.name}"
