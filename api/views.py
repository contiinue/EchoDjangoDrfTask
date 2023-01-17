from django.utils import timezone
from asgiref.sync import async_to_sync
from django.contrib.auth import login
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import BasicAuthentication
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
from .auth_classes import SessionCsrfExemptAuthentication
from .serializers import RegistrationSerializer, LoginSerializer, EchoSerializer
from .models import Message
from .utils import get_new_token


class RegistrationView(CreateAPIView, ViewSet):
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        """After registration, login() user to site"""
        user = serializer.save()
        user.token = get_new_token()
        user.save()
        login(self.request, user)


class LoginView(ViewSet):
    serializer_class = LoginSerializer
    authentication_classes = (SessionCsrfExemptAuthentication, BasicAuthentication)

    @swagger_auto_schema(method="post", request_body=LoginSerializer)
    @action(methods=["post"], detail=False, url_path="")
    def login(self, request):
        serializer = self.serializer_class(data=request.data)
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

    @action(
        methods=["get"], detail=False, url_path="reset_token", url_name="reset_token"
    )
    def reset_token(self, request):
        new_token = get_new_token()
        request.user.token.delete()
        request.user.token = new_token
        request.user.save()
        return Response({"token": new_token.token}, status=HTTP_200_OK)

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
        """Get telegram user_id, and validate date authorization,
        if date create token > N days(set in settings), will raise ValidationError.
        """
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
