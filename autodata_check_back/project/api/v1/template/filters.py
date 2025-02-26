from django.db.models import Q  # noqa: WPS347
from django_filters import CharFilter, FilterSet

from apps.template.models import Template


class TemplateFilterSet(FilterSet):
    title_search = CharFilter(method='search_by_title', help_text='Поиск по названию')
    fio_search = CharFilter(method='search_by_fio', help_text='Поиск по ФИО')
    phone_search = CharFilter(method='search_by_phone', help_text='Поиск по номеру телефона')

    class Meta:
        model = Template
        fields = ('is_main', 'is_accreditation')

    def search_by_title(self, queryset, name, value):
        if value:
            return queryset.filter(title__icontains=value)

    def search_by_fio(self, queryset, name, value):
        if value:
            for svalue in value.split(' '):
                queryset = queryset.filter(
                    Q(user__first_name__icontains=svalue)
                    | Q(user__last_name__icontains=svalue)
                    | Q(user__middle_name__icontains=svalue),
                )
            return queryset

    def search_by_phone(self, queryset, name, value):
        if value:
            return queryset.filter(user__phone__icontains=value)
