from constance import config
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from apps.file.models import DBFile, File, Image, StaticFile
from apps.helpers.batchmixin import DeleteBatchMixin
from apps.helpers.exceptions import BadRequestResponseSerializer
from apps.helpers.viewsets import ExtendedModelViewSet

from .serializers import DBFileSerializer, FileSerializer, ImageSerializer, StaticFileSerializer


class FileViewSet(ExtendedModelViewSet, DeleteBatchMixin):
    queryset = File.objects.all().non_deleted()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(responses={200: StaticFileSerializer(many=True)})
    @action(methods=['get'], detail=False, url_path='static-files')
    def static_files(self, request):
        queryset = StaticFile.objects.all()
        return Response(StaticFileSerializer(queryset, many=True, context={'request': request}).data)


class ImageViewSet(ExtendedModelViewSet, DeleteBatchMixin):
    queryset = Image.objects.all().non_deleted()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser,)


class DBFileViewSet(viewsets.ViewSet):

    @swagger_auto_schema(
        responses={
            200: DBFileSerializer,
            400: BadRequestResponseSerializer,
        },
    )
    def list(self, request):
        """Отдает файл с БД."""
        instance = DBFile.objects.first()  # noqa: DAR401
        if not instance:
            raise ValidationError({'error': config.FILE_DB_FILE_NOT_FOUND_ERROR})
        serializer = DBFileSerializer(instance=instance, context=self.get_renderer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)
