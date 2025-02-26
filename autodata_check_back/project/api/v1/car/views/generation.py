from rest_framework import mixins, permissions

from api.v1.car.filters.generation import GenerationFilterSet
from api.v1.car.serializers.generation import GenerationReadSerializer
from apps.car.models.generation import Generation
from apps.helpers.viewsets import ExtendedViewSet


class GenerationViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, ExtendedViewSet):
    queryset = Generation.objects.all()
    serializer_class = GenerationReadSerializer
    serializer_class_map = {
        'list': GenerationReadSerializer,
        'retrieve': GenerationReadSerializer,
    }

    filterset_class = GenerationFilterSet
    permission_classes = (permissions.IsAuthenticated,)
