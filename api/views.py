from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.generics import CreateAPIView
from .serializers import RegistrationSerializer, LoginSerializer


class RegistrationView(CreateAPIView, ViewSet):
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        login(self.request, serializer.save())


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.POST)
        serializer.is_valid(raise_exception=True)
        login(request, serializer.validated_data["user"])
        return Response(data={"success": "u in system :)"}, status=HTTP_200_OK)
