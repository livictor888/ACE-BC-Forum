from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """user model that we use to create a new users"""
    email = models.EmailField(unique=True)
    is_subscribed = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    is_subscribed = models.BooleanField(default=False)
