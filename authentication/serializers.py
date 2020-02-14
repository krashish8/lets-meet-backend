from rest_framework import serializers
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

def create_auth_token(user):
    token, created = Token.objects.get_or_create(user=user)
    return token


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid Credentials!")
        return data

    def get_token(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        return TokenSerializer({
            'token': create_auth_token(user)
        })


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=256)

    def validate_email(self, email):
        if User.objects.filter(email=email):
            raise serializers.ValidationError("Email already exists")
        return email

    def register(self):
        data = self.validated_data
        email = data['email']
        first_name = data['first_name']
        last_name = data['last_name']
        password = data['password']

        user = User.objects.create_user(username=email, password=password)
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return TokenSerializer({
            'token': create_auth_token(user)
        })

    class Meta:
        model = User
        fields = ('email','first_name','last_name','password')
