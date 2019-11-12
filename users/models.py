from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(default='', blank=True)
    phone = models.CharField(max_length=50, blank=True)
