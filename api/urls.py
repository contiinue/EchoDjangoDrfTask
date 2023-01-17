from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistrationView, LoginView, EchoTelegram

router = DefaultRouter()
router.register("registration", RegistrationView, basename="registration")
router.register("echo", EchoTelegram, basename="echo")
router.register('', LoginView, basename='login')

urlpatterns = [
    path("", include(router.urls)),
]
