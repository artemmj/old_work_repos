from rest_framework import mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.car.filters.model import ModelFilterSet
from api.v1.car.serializers.model import ModelReadSerializer, ModelYearsSerializer
from apps.car.models.model import Model
from apps.helpers.viewsets import ExtendedViewSet


class ModelViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, ExtendedViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelReadSerializer
    serializer_class_map = {
        'list': ModelReadSerializer,
        'retrieve': ModelReadSerializer,
        'years': ModelYearsSerializer,
    }

    filterset_class = ModelFilterSet
    permission_classes = (permissions.IsAuthenticated,)
    search_fields = ('title',)
    ordering_fields = ('title', 'popular')

    @action(methods=['get'], detail=True)
    def years(self, request, *args, **kwargs):
        """Года выпуска модели."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
