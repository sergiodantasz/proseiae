from django.contrib.auth.models import User


def set_admin_user(username):
    user = User.objects.filter(username=username).first()
    if user:
        user.is_staff = True
        user.is_superuser = True
        user.save()
