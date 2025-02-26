from rest_framework import mixins, permissions

from api.v1.car.filters.brand import BrandFilterSet
from api.v1.car.serializers.brand import BrandSerializer
from apps.car.models.brand import Brand
from apps.helpers.viewsets import ExtendedViewSet


class BrandViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, ExtendedViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    serializer_class_map = {
        'list': BrandSerializer,
        'retrieve': BrandSerializer,
    }

    filterset_class = BrandFilterSet
    permission_classes = (permissions.IsAuthenticated,)
    search_fields = ('title',)
    ordering_fields = ('title', 'popular')

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset).distinct()
