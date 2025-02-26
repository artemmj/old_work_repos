from django.db.models import Q  # noqa: WPS347
from django_filters import CharFilter, DateFilter, FilterSet

from apps.inspection_task.models.task import InspectionTaskCar


class InspectionTaskCarFilterSet(FilterSet):
    brand_model_search = CharFilter(method='search_by_brand_model', help_text='Поиск по названию марки и модели')
    vin_code_search = CharFilter(method='search_by_vin_code', help_text='Поиск по номеру ВИН')
    fio_search = CharFilter(method='search_by_fio', help_text='Поиск по ФИО инспектора')
    organization_title_search = CharFilter(
        method='search_by_organization_title',
        help_text='Поиск по названию организации',
    )
    task_created_at = DateFilter(method='get_task_created_at')
    task_status = CharFilter(method='search_by_task_status')

    class Meta:
        model = InspectionTaskCar
        fields = ('task_created_at',)

    def search_by_brand_model(self, queryset, name, value):
        if value:
            for svalue in value.split(' '):
                queryset = queryset.filter(Q(brand__title__icontains=svalue) | Q(model__title__icontains=svalue))
            return queryset

    def search_by_vin_code(self, queryset, name, value):
        if value:
            return queryset.filter(vin_code__icontains=value)

    def search_by_fio(self, queryset, name, value):
        if value:
            for svalue in value.split(' '):
                queryset = queryset.filter(
                    Q(task__inspector__first_name__icontains=svalue)
                    | Q(task__inspector__last_name__icontains=svalue)
                    | Q(task__inspector__middle_name__icontains=svalue),
                )
            return queryset

    def search_by_organization_title(self, queryset, name, value):
        if value:
            return queryset.filter(task__organization__title__icontains=value)

    def get_task_created_at(self, queryset, name, value):
        if value:
            return queryset.filter(task__created_at__date=value)

    def search_by_task_status(self, queryset, name, value):
        splitted = value.split(',')
        queryset = queryset.filter(task__status__in=splitted).order_by('-task__status')
        return queryset
