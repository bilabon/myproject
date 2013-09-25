from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username, password and email are required. Other fields are optional.
    """
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
