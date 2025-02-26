import logging

from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer,
    RefreshJSONWebTokenSerializer,
    VerifyJSONWebTokenSerializer,
)
from rest_framework_jwt.settings import api_settings

from apps.helpers.batchmixin import DeleteBatchMixin
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.viewsets import RUDExtendedModelViewSet
from apps.user.managers import UserManager

from . import serializers
from .filters import UserFilterSet

User = get_user_model()
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
logger = logging.getLogger()


class UserViewSet(RUDExtendedModelViewSet, DeleteBatchMixin):  # noqa: WPS338 WPS214
    queryset = User.objects.all()
    serializer_class = serializers.UserWriteSerializer
    serializer_class_map = {
        'list': serializers.UserReadSerializer,
        'retrieve': serializers.UserReadSerializer,
        'me': serializers.UserReadSerializer,
        'login': JSONWebTokenSerializer,
        'refresh': RefreshJSONWebTokenSerializer,
        'verify': VerifyJSONWebTokenSerializer,
        'change_password': serializers.UserChangePasswordSerializer,
        'compact': serializers.UserCompactSerializer,
    }
    permission_map = {
        'login': permissions.AllowAny,
    }
    permission_classes = (permissions.IsAuthenticated,)
    search_fields = ('first_name', 'middle_name', 'last_name')
    ordering_fields = ('first_name', 'middle_name', 'last_name')
    filterset_class = UserFilterSet
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

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

    def _auth(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.object.get('token')
        return Response({'token': token})

    @swagger_auto_schema(responses=default_responses)
    @action(methods=['post'], detail=False)
    def login(self, request):
        """Retrieve auth token by pair of username & password."""
        return self._auth(request)

    @swagger_auto_schema(responses=default_responses)
    @action(methods=['post'], detail=False)
    def refresh(self, request):
        """Refresh auth token by exist."""
        return self._auth(request)

    @swagger_auto_schema(responses=default_responses)
    @action(methods=['post'], detail=False)
    def verify(self, request):
        """Verify auth token by exist."""
        return self._auth(request)

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

    @action(methods=['get'], detail=False)
    def compact(self, request):
        """List compact user."""
        return super().list(request)  # noqa: WPS613
