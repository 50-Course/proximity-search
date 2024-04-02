"""
This module contains the serializers for shared models across the project.

This include the serializers for the following models:

-  User
- Profile (User Profile for the User model)
- Token (Token model for the User model)
- Authentication and Authorization Serializers
- APIKey (APIKey model for a User model, an API Key is used to authenticate a user to the API)
"""

from django.conf import settings
from django.contrib.auth.models import update_last_login
from django.db.models import fields
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token

from .exceptions import ObjectDoesNotExistException
from .models import User, UserProfile

User = settings.AUTH_USER_MODEL


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class ProfileSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    bio = serializers.CharField()
    token  = serializers.CharField()
    api_key = serializers.CharField()

    class Meta:
        extra_kwargs = {
            'name': {'required': True},
            'email': {'required': True},
            'bio': {'required': False},
            'api_key': {'required': False},
        }

    def create(self, validated_data):
        return UserProfile.objects.create(**validated_data)

class UserProfileWriteSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    bio = serializers.CharField(max_length=1000)


class SignInSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh_token = self.get_token(self.user)
        data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh_token)
        data['access'] = str(refresh_token.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

class SignupSerializer(UserSerializer):

    def create(self, validated_data):
        try:
            user = User.objects.get(email=validated_data['email'])
        except ObjectDoesNotExistException:
            user = User.objects.create_user(**validated_data)
        return user
