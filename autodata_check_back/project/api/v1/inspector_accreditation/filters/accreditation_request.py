from django.db.models import Q  # noqa: WPS347
from django_filters import CharFilter, FilterSet

from apps.inspector_accreditation.models import InspectorAccreditationRequest


class AccreditationRequestFilterSet(FilterSet):
    fio = CharFilter(method='search_fio')
    inn = CharFilter(method='search_inn')
    company = CharFilter(method='search_company')
    city_title = CharFilter(method='search_city_title')

    class Meta:
        model = InspectorAccreditationRequest
        fields = ('accreditation_inspection__status', 'fio', 'inn', 'work_skills', 'company', 'radius')

    def search_fio(self, queryset, name, value):  # noqa: WPS110
        if value:
            return queryset.filter(Q(user__first_name__icontains=value) | Q(user__last_name__icontains=value))
        return queryset

    def search_inn(self, queryset, name, value):  # noqa: WPS110
        if value:
            return queryset.filter(inn__icontains=value)
        return queryset

    def search_company(self, queryset, name, value):  # noqa: WPS110
        if value:
            return queryset.filter(company__icontains=value)
        return queryset

    def search_city_title(self, queryset, name, value):  # noqa: WPS110
        if value:
            return queryset.filter(city__title__icontains=value)
        return queryset
