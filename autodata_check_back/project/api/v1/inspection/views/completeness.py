from rest_framework import permissions

from api.v1.inspection.serializers.completeness import CompletenessReadSerializer, CompletenessWriteSerializer
from apps.helpers.viewsets import ExtendedModelViewSet
from apps.inspection.models.completeness import Completeness


class CompletenessViewSet(ExtendedModelViewSet):
    """Комплектность."""

    queryset = Completeness.objects.all()
    serializer_class = CompletenessReadSerializer
    serializer_class_map = {
        'list': CompletenessReadSerializer,
        'create': CompletenessWriteSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
