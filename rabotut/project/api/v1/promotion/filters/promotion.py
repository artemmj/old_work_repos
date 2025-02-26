from django_filters import BooleanFilter, FilterSet

from apps.promotion.models import Promotion


class PromotionFilter(FilterSet):
    is_published = BooleanFilter(field_name='mailings__is_published')

    class Meta:
        model = Promotion
        fields = ('type', 'is_hidden', 'is_main_display')
