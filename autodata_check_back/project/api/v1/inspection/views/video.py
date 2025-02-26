from rest_framework import permissions

from api.v1.inspection.serializers.video import VideoReadSerializer, VideoWriteSerializer
from apps.helpers.viewsets import ExtendedModelViewSet
from apps.inspection.models.video import Video


class VideoViewSet(ExtendedModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoReadSerializer
    serializer_class_map = {
        'create': VideoWriteSerializer,
        'update': VideoWriteSerializer,
        'partial_update': VideoWriteSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
