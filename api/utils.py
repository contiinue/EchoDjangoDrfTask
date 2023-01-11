from django.utils import timezone

from api.models import Token
from echo.settings import TOKEN_LIFE_DAYS


def get_new_token() -> Token:
    return Token.objects.create(
        date_end=timezone.now() + timezone.timedelta(days=TOKEN_LIFE_DAYS)
    )
