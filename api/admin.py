from django.contrib import admin
from .models import Token, Message, User

admin.site.register(Token)
admin.site.register(Message)
admin.site.register(User)
