from rest_framework import permissions

from api.v1.inspection.serializers.lift import LiftReadSerializer, LiftWriteSerializer
from apps.helpers.viewsets import ExtendedModelViewSet
from apps.inspection.models.lift import Lift


class LiftViewSet(ExtendedModelViewSet):
    """Осмотры на подъемнике."""

    queryset = Lift.objects.all()
    serializer_class = LiftReadSerializer
    serializer_class_map = {
        'list': LiftReadSerializer,
        'retrieve': LiftReadSerializer,
        'create': LiftWriteSerializer,
        'update': LiftWriteSerializer,
        'partial_update': LiftWriteSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
