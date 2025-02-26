from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.arketa.clients import ArketaFileApiClient
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.user.permissions import IsApplicantConfirmedPermission, IsApplicantPermission, IsMasterPermission

from ..serializers import FileArketaExtendedSerializer, FileArketaUploadSerializer


class ArketaFileViewSet(ViewSet):
    permission_classes = (IsApplicantConfirmedPermission | IsApplicantPermission | IsMasterPermission,)
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        request_body=FileArketaUploadSerializer(),
        responses={
            status.HTTP_200_OK: FileArketaExtendedSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        })
    def create(self, request):  # noqa: WPS110
        serializer = FileArketaUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = request.META.get('HTTP_AUTHORIZATION')
        return Response(ArketaFileApiClient(token).create_file(serializer.validated_data))

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: FileArketaExtendedSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        })
    def retrieve(self, request, pk=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        return Response(ArketaFileApiClient(token).get_file(pk))

    @swagger_auto_schema(
        request_body=FileArketaUploadSerializer(),
        responses={
            status.HTTP_200_OK: FileArketaExtendedSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        })
    def update(self, request, pk=None):
        serializer = FileArketaUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = request.META.get('HTTP_AUTHORIZATION')
        return Response(ArketaFileApiClient(token).put_file(pk, serializer.validated_data))

    @swagger_auto_schema(
        request_body=FileArketaUploadSerializer(),
        responses={
            status.HTTP_200_OK: FileArketaExtendedSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        })
    def partial_update(self, request, pk=None):
        serializer = FileArketaUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = request.META.get('HTTP_AUTHORIZATION')
        return Response(ArketaFileApiClient(token).patch_file(pk, serializer.validated_data))

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: FileArketaExtendedSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        })
    def destroy(self, request, pk=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        return Response(ArketaFileApiClient(token).delete_file(pk))
