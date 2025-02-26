from rest_framework import mixins, permissions

from api.v1.inspection.serializers.damage import DamageReadSerializer, DamageWriteSerializer
from apps.helpers.viewsets import ExtendedModelViewSet
from apps.inspection.models.damage import Damage


class DamageViewSet(ExtendedModelViewSet):
    """Повреждения."""

    queryset = Damage.objects.all()
    serializer_class = DamageWriteSerializer
    serializer_class_map = {
        'list': DamageReadSerializer,
        'create': DamageWriteSerializer,
        'retrieve': DamageReadSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
