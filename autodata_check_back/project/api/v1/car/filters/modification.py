from django_filters import FilterSet

from apps.car.models import Modification


class ModificationFilterSet(FilterSet):

    class Meta:
        model = Modification
        fields = [
            'brand',
            'model',
            'generation',
            'year_start',
            'year_end',
            'drive_type',
            'engine_type',
            'gearbox_type',
            'body_type',
        ]
