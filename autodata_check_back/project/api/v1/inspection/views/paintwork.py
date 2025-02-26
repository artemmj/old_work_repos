from rest_framework import permissions

from api.v1.inspection.serializers.paintwork import PaintworkReadSerializer, PaintworkWriteSerializer
from apps.helpers.viewsets import ExtendedModelViewSet
from apps.inspection.models.paintwork import Paintwork


class PaintWorkViewSet(ExtendedModelViewSet):
    """Лакокрасочное покрытие."""

    queryset = Paintwork.objects.all()
    serializer_class = PaintworkWriteSerializer
    serializer_class_map = {
        'list': PaintworkReadSerializer,
        'create': PaintworkWriteSerializer,
        'retrieve': PaintworkReadSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
