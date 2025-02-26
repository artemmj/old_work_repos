from django_filters import FilterSet

from apps.document.models import Inn


class InnFilterSet(FilterSet):
    class Meta:
        model = Inn
        fields = ('user', 'status')
