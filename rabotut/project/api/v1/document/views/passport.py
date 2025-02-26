from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.document.models import Passport
from apps.document.services import AcceptDocumentService, DeclineDocumentService, PassportRecognitionService
from apps.file.models import File
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.serializers import EmptySerializer
from apps.helpers.viewsets import CRUDExtendedModelViewSet
from apps.user.permissions import IsApplicantConfirmedPermission, IsApplicantPermission, IsMasterPermission

from ..filters import PassportFilterSet
from ..serializers import (
    PassportReadSerializer,
    PassportRecognitionResponseSerializer,
    PassportRecognitionSerializer,
    PassportWriteSerializer,
)
from ..serializers.all_documents import DeclineDocumentSerializer

DEFAULT_SINGLE_READ_RESPONSES = {
    status.HTTP_200_OK: PassportReadSerializer(),
    status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
    status.HTTP_404_NOT_FOUND: ErrorResponseSerializer(many=True),
}


class PassportViewSet(CRUDExtendedModelViewSet):  # noqa: WPS214
    queryset = Passport.objects.non_deleted()
    serializer_class = PassportReadSerializer
    serializer_class_map = {
        'create': PassportWriteSerializer,
        'decline': DeclineDocumentSerializer,
        'update': PassportWriteSerializer,
        'partial_update': PassportWriteSerializer,
        'recognition': PassportRecognitionSerializer,
    }
    filterset_class = PassportFilterSet
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
        operation_summary='Получение Паспорта',
        responses={
            status.HTTP_200_OK: PassportReadSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
            status.HTTP_404_NOT_FOUND: ErrorResponseSerializer(many=True),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Создание Паспорта',
        request_body=PassportWriteSerializer,
        responses=DEFAULT_SINGLE_READ_RESPONSES,
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(PassportReadSerializer(instance).data)

    @swagger_auto_schema(
        operation_summary='Обновить Паспорт',
        request_body=PassportWriteSerializer,
        responses=DEFAULT_SINGLE_READ_RESPONSES,
    )
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(PassportReadSerializer(instance).data)

    @swagger_auto_schema(
        operation_summary='Обновить Паспорт',
        request_body=PassportWriteSerializer,
        responses=DEFAULT_SINGLE_READ_RESPONSES,
    )
    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(PassportReadSerializer(instance).data)

    @swagger_auto_schema(
        operation_summary='Принять документ Паспорт',
        request_body=EmptySerializer(),
        responses=DEFAULT_SINGLE_READ_RESPONSES,
    )
    @action(methods=['post'], detail=True, url_path='accept')
    def accept(self, request, pk=None):
        instance = self.get_object()
        AcceptDocumentService(document=instance).process()
        return Response(PassportReadSerializer(self.get_object()).data)

    @swagger_auto_schema(
        operation_summary='Отклонить Паспорт',
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
        return Response(PassportReadSerializer(self.get_object()).data)

    @swagger_auto_schema(
        operation_summary='Распознать Паспорт',
        request_body=PassportRecognitionSerializer(),
        responses={
            status.HTTP_200_OK: PassportRecognitionResponseSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
            status.HTTP_404_NOT_FOUND: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['post'], detail=False, url_path='recognition')
    def recognition(self, request):
        request_serializer = self.get_serializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        passport_file = File.objects.get(pk=request_serializer.data.get('file'))
        recognition_result = PassportRecognitionService(passport_file).process()
        recognition_result['file'] = passport_file.pk
        return Response(recognition_result)
