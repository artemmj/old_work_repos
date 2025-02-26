import logging

from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.viewsets import RUDExtendedModelViewSet
from apps.user.managers import UserManager

from . import serializers

User = get_user_model()
logger = logging.getLogger()


class UserViewSet(RUDExtendedModelViewSet):  # noqa: WPS338 WPS214
    queryset = User.objects.all()
    serializer_class = serializers.UserWriteSerializer
    serializer_class_map = {
        'list': serializers.UserReadSerializer,
        'retrieve': serializers.UserReadSerializer,
        'me': serializers.UserReadSerializer,
        'change_password': serializers.UserChangePasswordSerializer,
    }
    permission_map = {
        'login': permissions.AllowAny,
    }
    permission_classes = (permissions.IsAuthenticated,)

    default_responses = {
        200: serializers.UserLoginResponseSerializer,
        400: ErrorResponseSerializer,
        410: ErrorResponseSerializer,
    }

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return User.objects.none()

        return UserManager().get_queryset(user)

    @action(methods=['post'], detail=False)
    def registration(self, request):
        """Register user."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializers.UserReadSerializer(instance=user, context=self.get_serializer_context()).data  # noqa: WPS110
        return Response(data, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False)
    def me(self, request, **kwargs):
        """Retrieve logged user information."""
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: serializers.UserChangePasswordSerializer, 400: ErrorResponseSerializer})
    @action(methods=['post'], detail=False, url_path='change-password')
    def change_password(self, request):
        """Change password."""
        serializer = self.get_serializer(data=request.data, instance=request.user)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializers.UserReadSerializer(instance=user).data  # noqa: WPS110
        return Response(data)
