from django.utils import timezone
from asgiref.sync import async_to_sync
from django.contrib.auth import login
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.generics import CreateAPIView, ListAPIView

from echo.settings import TOKEN_LIFE_DAYS
from bot.main import send_message
from .serializers import RegistrationSerializer, LoginSerializer, EchoSerializer
from .models import Token, Message


class RegistrationView(CreateAPIView, ViewSet):
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.token = self.get_token()
        user.save()
        login(self.request, user)

    @staticmethod
    def get_token() -> Token:
        return Token.objects.create(
            date_end=timezone.now() + timezone.timedelta(days=TOKEN_LIFE_DAYS)
        )


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.POST)
        serializer.is_valid(raise_exception=True)
        login(request, serializer.validated_data["user"])
        return Response(data={"success": "u in system :)"}, status=HTTP_200_OK)


class EchoTelegram(ListAPIView, ViewSet):
    serializer_class = EchoSerializer
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()

    @action(methods=["get"], detail=False, url_path="get_token", url_name="get_token")
    def get_token(self, request):
        return Response({"token": request.user.token.token}, status=HTTP_200_OK)

    @action(methods=["post"], detail=False, url_path="", url_name="")
    def send_message(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        async_to_sync(send_message)(
            self.get_user_id(),
            request.user.first_name,
            serializer.validated_data["message"],
        )
        self.save_message(serializer.validated_data["message"])
        return Response(data=serializer.data)

    def get_user_id(self) -> str:
        user_id = self.request.user.token.telegram_id
        if not user_id or (
            timezone.now().date() - self.request.user.token.date_end
        ) > timezone.timedelta(days=TOKEN_LIFE_DAYS):
            raise ValidationError("Токен истек или не был авторизован в телеграмме.")
        return user_id

    def save_message(self, message):
        msg = Message.objects.create(message=message)
        self.request.user.massages.add(msg)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
