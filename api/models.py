from django.contrib.auth.models import AbstractUser
from django.db import models
from .fields import TokenAutorizateField


class User(AbstractUser):
    massages = models.ManyToManyField("Message")
    token = models.ForeignKey("Token", on_delete=models.CASCADE, null=True)


class Message(models.Model):
    message = models.CharField(max_length=127)
    date_massage = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Дата сообщения: {self.date_massage}: Сообщение: {self.message}>"


class Token(models.Model):
    """Authorization token for telegram bot"""

    token = TokenAutorizateField(max_length=33, unique=True)
    telegram_id = models.CharField(max_length=120)
    data_create = models.DateField(auto_now=True)
    date_end = models.DateField()

    def __str__(self):
        return self.token
