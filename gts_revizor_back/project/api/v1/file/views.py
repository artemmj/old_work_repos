from rest_framework.parsers import MultiPartParser

from apps.file.models import File, Image
from apps.helpers.batchmixin import DeleteBatchMixin
from apps.helpers.viewsets import ExtendedModelViewSet

from .serializers import FileSerializer, ImageSerializer


class FileViewSet(ExtendedModelViewSet, DeleteBatchMixin):
    queryset = File.objects.all().non_deleted()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser,)


class ImageViewSet(ExtendedModelViewSet, DeleteBatchMixin):
    queryset = Image.objects.all().non_deleted()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser,)
