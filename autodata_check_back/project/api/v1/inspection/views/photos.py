from rest_framework import permissions

from api.v1.inspection.serializers.photos import PhotosReadSerializer, PhotosWriteSerializer
from apps.helpers.viewsets import ExtendedModelViewSet
from apps.inspection.models.photos import Photos


class PhotosViewSet(ExtendedModelViewSet):
    queryset = Photos.objects.all()
    serializer_class = PhotosWriteSerializer
    serializer_class_map = {
        'list': PhotosReadSerializer,
        'retrieve': PhotosReadSerializer,
        'create': PhotosWriteSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)

    default_responses = {
        201: PhotosReadSerializer,
    }
