from drf_yasg.utils import swagger_auto_schema  # noqa: WPS201
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.document.models import Selfie
from apps.document.services import AcceptDocumentService, DeclineDocumentService
from apps.document.services.confirm_selfie_passport import ConfirmSelfiePassportService
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.serializers import EmptySerializer
from apps.helpers.viewsets import CRUDExtendedModelViewSet
from apps.user.permissions import IsApplicantConfirmedPermission, IsApplicantPermission, IsMasterPermission

from ..filters import SelfieFilterSet
from ..serializers import SelfieReadSerializer, SelfieWriteSerializer
from ..serializers.all_documents import DeclineDocumentSerializer
from ..serializers.selfie import AcceptPassportSerializer

DEFAULT_SINGLE_READ_RESPONSES = {
    status.HTTP_200_OK: SelfieReadSerializer(),
    status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
    status.HTTP_404_NOT_FOUND: ErrorResponseSerializer(many=True),
}


class SelfieViewSet(CRUDExtendedModelViewSet):  # noqa: WPS214
    queryset = Selfie.objects.non_deleted()
    serializer_class = SelfieReadSerializer
    serializer_class_map = {
        'create': SelfieWriteSerializer,
        'decline': DeclineDocumentSerializer,
        'confirm_passport': AcceptPassportSerializer,
        'update': SelfieWriteSerializer,
        'partial_update': SelfieWriteSerializer,
    }
    filterset_class = SelfieFilterSet
    permission_classes = (IsAuthenticated,)
    permission_map = {
        'accept': IsMasterPermission,
        'decline': IsMasterPermission,
        'confirm_passport': IsMasterPermission,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if IsMasterPermission().has_permission(self.request, self):
            return queryset
        if (IsApplicantPermission | IsApplicantConfirmedPermission)().has_permission(self.request, self):
            return queryset.filter(user=self.request.user)
        return queryset.none()

    @swagger_auto_schema(
        operation_summary='Получение Селфи',
        responses={
            status.HTTP_200_OK: SelfieReadSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
            status.HTTP_404_NOT_FOUND: ErrorResponseSerializer(many=True),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Создание Селфи',
        request_body=SelfieWriteSerializer,
        responses=DEFAULT_SINGLE_READ_RESPONSES,
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(SelfieReadSerializer(instance).data)

    @swagger_auto_schema(
        operation_summary='Обновить Селфи',
        request_body=SelfieWriteSerializer,
        responses=DEFAULT_SINGLE_READ_RESPONSES,
    )
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(SelfieReadSerializer(instance).data)

    @swagger_auto_schema(
        operation_summary='Обновить Селфи',
        request_body=SelfieWriteSerializer,
        responses=DEFAULT_SINGLE_READ_RESPONSES,
    )
    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(SelfieReadSerializer(instance).data)

    @swagger_auto_schema(
        operation_summary='Принять документ Селфи',
        request_body=EmptySerializer(),
        responses=DEFAULT_SINGLE_READ_RESPONSES,
    )
    @action(methods=['post'], detail=True, url_path='accept')
    def accept(self, request, pk=None):
        instance = self.get_object()
        AcceptDocumentService(document=instance).process()
        return Response(SelfieReadSerializer(self.get_object()).data)

    @swagger_auto_schema(
        operation_summary='Отклонить Селфи',
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
        return Response(SelfieReadSerializer(self.get_object()).data)

    @swagger_auto_schema(
        operation_summary='Подтверждение соответствия',
        request_body=AcceptPassportSerializer,
        responses=DEFAULT_SINGLE_READ_RESPONSES,
    )
    @action(methods=['post'], detail=True, url_path='confirm_passport')
    def confirm_passport(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        selfie = self.get_object()
        passport = serializer.data.get('passport')
        ConfirmSelfiePassportService().process(passport, selfie)
        return Response(SelfieReadSerializer(selfie).data)
