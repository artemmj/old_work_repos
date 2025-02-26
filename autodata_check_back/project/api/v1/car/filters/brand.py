from django_filters import FilterSet

from apps.car.models import Brand


class BrandFilterSet(FilterSet):

    class Meta:
        model = Brand
        fields = ['popular', 'models__category']
