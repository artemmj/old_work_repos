from django_filters import FilterSet

from apps.car.models import Generation
from apps.helpers.filters import IntegerFilter


class GenerationFilterSet(FilterSet):
    year = IntegerFilter(method='filter_by_year')

    class Meta:
        model = Generation
        fields = ['brand', 'model', 'category', 'year_start', 'year_end']

    def filter_by_year(self, queryset, name, value):
        if value:
            return queryset.filter(year_start__lte=value, year_end__gte=value)
