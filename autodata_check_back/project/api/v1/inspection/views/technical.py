from rest_framework import mixins, permissions

from api.v1.inspection.serializers.technical import TechnicalReadSerializer, TechnicalWriteSerializer
from apps.helpers.viewsets import ExtendedModelViewSet
from apps.inspection.models.technical import Technical


class TechnicalViewSet(ExtendedModelViewSet):
    """Тех.осмотры."""

    queryset = Technical.objects.all()
    serializer_class = TechnicalReadSerializer
    serializer_class_map = {
        'list': TechnicalReadSerializer,
        'retrieve': TechnicalReadSerializer,
        'create': TechnicalWriteSerializer,
        'update': TechnicalWriteSerializer,
        'partial_update': TechnicalWriteSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
