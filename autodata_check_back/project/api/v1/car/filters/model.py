from django_filters import FilterSet

from apps.car.models import Model


class ModelFilterSet(FilterSet):
    class Meta:
        model = Model
        fields = ['brand', 'popular', 'category']
