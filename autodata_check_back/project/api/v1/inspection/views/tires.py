from rest_framework import permissions

from api.v1.inspection.serializers.tires import TiresReadSerializer, TiresWriteSerializer
from apps.helpers.viewsets import ExtendedModelViewSet
from apps.inspection.models.tires import Tires


class TiresViewSet(ExtendedModelViewSet):
    """Шины."""

    queryset = Tires.objects.all()
    serializer_class = TiresReadSerializer
    serializer_class_map = {
        'list': TiresReadSerializer,
        'create': TiresWriteSerializer,
        'update': TiresWriteSerializer,
        'retrieve': TiresReadSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
