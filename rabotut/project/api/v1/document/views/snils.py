from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.document.models import Snils
from apps.document.services import AcceptDocumentService, DeclineDocumentService
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.serializers import EmptySerializer
from apps.helpers.viewsets import CRUDExtendedModelViewSet
from apps.user.permissions import IsApplicantConfirmedPermission, IsApplicantPermission, IsMasterPermission

from ..filters import SnilsFilterSet
from ..serializers import SnilsReadSerializer, SnilsWriteSerializer
from ..serializers.all_documents import DeclineDocumentSerializer

DEFAULT_SINGLE_READ_RESPONSES = {
    status.HTTP_200_OK: SnilsReadSerializer(),
    status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
    status.HTTP_404_NOT_FOUND: ErrorResponseSerializer(many=True),
}


class SnilsViewSet(CRUDExtendedModelViewSet):
    queryset = Snils.objects.non_deleted()
    serializer_class = SnilsReadSerializer
    serializer_class_map = {
        'create': SnilsWriteSerializer,
        'decline': DeclineDocumentSerializer,
        'update': SnilsWriteSerializer,
        'partial_update': SnilsWriteSerializer,
    }
    filterset_class = SnilsFilterSet
    permission_classes = (IsAuthenticated,)
    permission_map = {
        'accept': IsMasterPermission,
        'decline': IsMasterPermission,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if IsMasterPermission().has_permission(self.request, self):
            return queryset
        if (IsApplicantPermission | IsApplicantConfirmedPermission)().has_permission(self.request, self):
            return queryset.filter(user=self.request.user)
        return queryset.none()

    @swagger_auto_schema(
        operation_summary='Получение СНИЛС',
        responses={
            status.HTTP_200_OK: SnilsReadSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
            status.HTTP_404_NOT_FOUND: ErrorResponseSerializer(many=True),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Создание СНИЛС',
        request_body=SnilsWriteSerializer(),
        responses=DEFAULT_SINGLE_READ_RESPONSES,
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(SnilsReadSerializer(instance).data)

    @swagger_auto_schema(
        operation_summary='Обновить СНИЛС',
        request_body=SnilsWriteSerializer,
        responses=DEFAULT_SINGLE_READ_RESPONSES,
    )
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(SnilsReadSerializer(instance).data)

    @swagger_auto_schema(
        operation_summary='Обновить СНИЛС',
        request_body=SnilsWriteSerializer,
        responses=DEFAULT_SINGLE_READ_RESPONSES,
    )
    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(SnilsReadSerializer(instance).data)

    @swagger_auto_schema(
        operation_summary='Принять документ СНИЛС',
        request_body=EmptySerializer(),
        responses=DEFAULT_SINGLE_READ_RESPONSES,
    )
    @action(methods=['post'], detail=True, url_path='accept')
    def accept(self, request, pk=None):
        instance = self.get_object()
        AcceptDocumentService(document=instance).process()
        return Response(SnilsReadSerializer(self.get_object()).data)

    @swagger_auto_schema(
        operation_summary='Отклонить документ СНИЛС',
        request_body=DeclineDocumentSerializer,
        responses=DEFAULT_SINGLE_READ_RESPONSES,
    )
    @action(methods=['post'], detail=True, url_path='decline')
    def decline(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rejection_reason = serializer.data.get('rejection_reason')
        instance = self.get_object()
        DeclineDocumentService(document=instance, rejection_reason=rejection_reason).process()
        return Response(SnilsReadSerializer(self.get_object()).data)
