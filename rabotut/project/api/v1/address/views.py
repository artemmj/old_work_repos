from apps.address.models import City
from apps.helpers.viewsets import ListExtendedModelViewSet

from .filters import CityFilterSet
from .serializers import CitySerializer


class CityViewSet(ListExtendedModelViewSet):
    queryset = City.objects.non_deleted()
    serializer_class = CitySerializer
    search_fields = ('name',)
    filterset_class = CityFilterSet
