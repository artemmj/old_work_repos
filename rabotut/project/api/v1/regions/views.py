from rest_framework.permissions import IsAuthenticated

from apps.helpers.viewsets import ListExtendedModelViewSet
from apps.regions.models import Region

from .serializers import RegionSerializer


class RegionViewSet(ListExtendedModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = (IsAuthenticated,)
    search_fields = ('name',)
