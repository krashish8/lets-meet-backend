from rest_framework.response import Response
from .serializers import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import status
from rest_framework import permissions


class LoginView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.get_token()
        return Response(response.data, status.HTTP_200_OK)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)
    
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.register()
        return Response(response.data, status.HTTP_200_OK)
