from django.db.models import Q  # noqa: WPS347
from django_filters import BooleanFilter, CharFilter, FilterSet

from apps.inspection.models.inspection import Inspection
from apps.inspection_task.models.task import InspectorTaskTypes


class InspectionFilterSet(FilterSet):  # noqa: WPS214
    my = BooleanFilter(method='filter_by_inspector', help_text='Фильтрует только по своим осмотрам')
    by_task = BooleanFilter(
        method='filter_by_task',
        help_text='Фильтрует свои осмотры где есть задание и является инспектором задания',
    )
    self_inspection = BooleanFilter(method='filter_self_inspection', help_text='Фильтрует свои самостоятельные осмотры')
    by_task_inspector = BooleanFilter(
        method='filter_by_task_inspector',
        help_text='Фильтрует свои осмотры где юзер назначен инспектором организации',
    )
    brand_model_search = CharFilter(method='search_by_brand_model', help_text='Поиск по названию марки и модели')
    vin_code_search = CharFilter(method='search_by_vin_code', help_text='Поиск по номеру ВИН')
    fio_search = CharFilter(method='search_by_fio', help_text='Поиск по ФИО инспектора')
    organization_title_search = CharFilter(
        method='search_by_organization_title',
        help_text='Поиск по названию организации',
    )
    task_status = CharFilter(method='search_by_task_status')

    class Meta:
        model = Inspection
        fields = ('organization', 'status', 'is_public', 'type')

    def filter_by_inspector(self, queryset, name, value):  # noqa: WPS110
        if value:
            return queryset.filter(inspector=self.request.user)
        return queryset

    def filter_by_task(self, queryset, name, value):  # noqa: WPS110
        if value:
            return queryset.filter(
                inspector=self.request.user,
                task__isnull=False,
                task__inspector=self.request.user,
                task__type=InspectorTaskTypes.FOR_SEARCH_INSPECTOR,
            )
        return queryset

    def filter_self_inspection(self, queryset, name, value):  # noqa: WPS110
        if value:
            return queryset.filter(inspector=self.request.user, task__isnull=True)
        return queryset

    def filter_by_task_inspector(self, queryset, name, value):  # noqa: WPS110
        if value:
            return queryset.filter(
                inspector=self.request.user,
                task__isnull=False,
                task__inspector=self.request.user,
                task__type=InspectorTaskTypes.FOR_APPOINTMENT,
            )
        return queryset

    def search_by_brand_model(self, queryset, name, value):
        if value:
            for svalue in value.split(' '):
                queryset = queryset.filter(
                    Q(car__brand__title__icontains=svalue)
                    | Q(car__model__title__icontains=svalue),
                )
            return queryset

    def search_by_vin_code(self, queryset, name, value):
        if value:
            return queryset.filter(car__vin_code__icontains=value)

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

    def search_by_task_status(self, queryset, name, value):
        splitted = value.split(',')
        queryset = queryset.filter(task__status__in=splitted).order_by('-task__status')
        return queryset
