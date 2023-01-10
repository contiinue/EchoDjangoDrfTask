from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistrationView, LoginView

router = DefaultRouter()
router.register("registration", RegistrationView, basename="registration")

urlpatterns = [path("", include(router.urls)), path("login/", LoginView.as_view())]
