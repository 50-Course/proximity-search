from django.shortcuts import render
from rest_framework import serializers, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)


class _TokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.get('refresh')
        access_token = response.data.get('access')
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token
        }
        return response

class SignInViewset(viewsets.ModelViewSet, _TokenObtainPairView):
    permission_classes = ('AllowAny')
    http_method_names = [ 'post' ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            response = self.post(request, *args, **kwargs)
        except TokenError as e:
            raise  InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class SignUpViewset(viewsets.ModelViewSet, TokenObtainPairView):
    permission_classes = ('AllowAny')
    http_method_names = [ 'post' ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh_token = RefreshToken.for_user(user)
        response = {
            "refresh": str(refresh_token),
            "access": str(refresh_token.access_token)
        }

        return Response({
            "user": serializer.data,
            "access": response['access'],
            "refresh": response['refresh']
        }, status=status.HTTP_201_CREATED)

class RefreshViewset(viewsets.ViewSet, TokenRefreshView):
    permission_classes = ('AllowAny')
    http_method_names = [ 'post' ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            refresh = serializer.validated_data.get('refresh')
            token = RefreshToken(refresh)
        except TokenError as e:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
