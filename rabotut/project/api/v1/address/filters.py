from django_filters import CharFilter, FilterSet, OrderingFilter


class CityFilterSet(FilterSet):
    search_name = CharFilter(field_name='name', lookup_expr='icontains')

    ordering = OrderingFilter(
        fields=(
            ('name', 'name'),
        ),
    )
