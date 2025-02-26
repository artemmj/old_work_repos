import logging

from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.serializers import EnumSerializer
from apps.helpers.viewsets import RUDExtendedModelViewSet

from . import serializers
from .filters import UserFilterSet

User = get_user_model()
logger = logging.getLogger()


class UserViewSet(RUDExtendedModelViewSet):  # noqa: WPS338 WPS214
    queryset = User.objects.all()
    serializer_class = serializers.UserWriteSerializer
    serializer_class_map = {
        'list': serializers.UserReadSerializer,
        'retrieve': serializers.UserReadSerializer,
        'me': serializers.UserReadSerializer,
        'compact': serializers.UserCompactSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)

    ordering_fields = ('first_name', 'middle_name', 'last_name', 'phone', 'doc_status')
    filterset_class = UserFilterSet
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    @swagger_auto_schema(
        operation_summary='Список пользователей в компактном виде.',
        responses={
            status.HTTP_200_OK: serializers.UserCompactSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['get'], detail=False)
    def compact(self, request):
        """Список пользователей в компактном виде."""
        return super().list(request)  # noqa: WPS613

    @swagger_auto_schema(
        operation_summary='Получение информации о пользователе.',
        responses={
            status.HTTP_200_OK: serializers.UserReadSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['get'], detail=False)
    def me(self, request, **kwargs):
        """Получение информации о пользователе."""
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary='Получение списка возможных статусов документов юзера.',
        responses={
            status.HTTP_200_OK: EnumSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['get'], detail=False)
    def document_status_choices(self, request):
        """Получение списка возможных статусов документов юзера."""
        return Response(EnumSerializer(BaseUserDocumentStatuses, many=True).data)
