from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db.models import QuerySet


class CityFilterManager:
    def get_near_city(self, queryset: QuerySet, location: Point) -> QuerySet:
        """Получить кверисет городов, отсортированных по близости к координате."""
        return queryset.annotate(
            distance=Distance('location', location),
        ).order_by('distance')
