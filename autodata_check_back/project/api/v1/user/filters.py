from django.contrib.auth import get_user_model
from django.db.models import Q  # noqa: WPS347
from django_filters import BooleanFilter, CharFilter, DateFilter, DateTimeFilter, FilterSet

from apps.user.models import RoleChoices

User = get_user_model()


class UserFilterSet(FilterSet):
    search_login = CharFilter(method='filter_search_login')
    start_date = DateFilter(field_name='created_at', lookup_expr='gte')
    end_date = DateFilter(field_name='created_at', lookup_expr='lte')
    update_date = DateTimeFilter(field_name='updated_at', lookup_expr='gte')
    is_inspector = BooleanFilter(method='filter_is_inspector')

    class Meta:
        model = User
        fields = ('first_name', 'middle_name', 'last_name', 'email')

    def filter_search_login(self, queryset, name, value):  # noqa: WPS110
        return queryset.filter(Q(phone=value) or Q(email=value))

    def filter_is_inspector(self, queryset, name, value):
        if value is True:
            queryset = queryset.filter(roles__contains=[RoleChoices.INSPECTOR])
        if value is False:
            queryset = queryset.exclude(roles__contains=[RoleChoices.INSPECTOR])
        return queryset
