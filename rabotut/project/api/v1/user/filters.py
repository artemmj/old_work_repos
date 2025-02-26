from django.contrib.auth import get_user_model
from django.db.models import Q, QuerySet  # noqa: WPS347
from django_filters import CharFilter, ChoiceFilter, FilterSet

from apps.user.models.doc_statuses import UserDocStatuses

User = get_user_model()


class UserFilterSet(FilterSet):
    search_email = CharFilter(method='filter_search_email')
    search_phone = CharFilter(method='filter_search_phone')
    search_fio = CharFilter(method='filter_search_fio')
    doc_status = ChoiceFilter(choices=UserDocStatuses.choices)

    class Meta:
        model = User
        fields = ('first_name', 'middle_name', 'last_name', 'email')

    def filter_search_email(self, queryset: QuerySet, name: str, value: str) -> QuerySet:  # noqa: WPS110
        return queryset.filter(email__icontains=value)

    def filter_search_phone(self, queryset: QuerySet, name: str, value: str) -> QuerySet:  # noqa: WPS110
        return queryset.filter(phone__icontains=value)

    def filter_search_fio(self, queryset: QuerySet, name: str, value: str) -> QuerySet:  # noqa: WPS110
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(middle_name__icontains=value),
        )
