from django_filters import FilterSet

from apps.document.models import Snils


class SnilsFilterSet(FilterSet):
    class Meta:
        model = Snils
        fields = ('user', 'status')
