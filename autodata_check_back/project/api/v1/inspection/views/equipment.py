from rest_framework import permissions

from api.v1.inspection.serializers.equipment import EquipmentReadSerializer, EquipmentWriteSerializer
from apps.helpers.viewsets import ExtendedModelViewSet
from apps.inspection.models.equipment import Equipment


class EquipmentViewSet(ExtendedModelViewSet):
    """Комплектация."""

    queryset = Equipment.objects.all()
    serializer_class = EquipmentWriteSerializer
    serializer_class_map = {
        'list': EquipmentReadSerializer,
        'create': EquipmentWriteSerializer,
        'retrieve': EquipmentReadSerializer,
        'update': EquipmentWriteSerializer,
        'partial_update': EquipmentWriteSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
