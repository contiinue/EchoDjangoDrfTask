from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    massages = models.ManyToManyField("Message")


class Message(models.Model):
    massage = models.CharField(max_length=127)
    date_massage = models.DateTimeField(auto_now=True)
