from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistrationView, LoginView, EchoTelegram

router = DefaultRouter()
router.register("registration", RegistrationView, basename="registration")
router.register("echo", EchoTelegram, basename="echo")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginView.as_view()),
    # path('echo/', EchoTelegram.as_view())
]
