from django.db.models import Q  # noqa: WPS347
from django_filters import BooleanFilter, CharFilter, FilterSet

from apps.inspection_task.models.task import InspectionTask, InspectionTaskCar, InspectorTaskTypes


class InspectionTaskFilterSet(FilterSet):
    is_inspector = BooleanFilter(method='filter_is_inspector')
    is_author = BooleanFilter(method='filter_is_author')

    class Meta:
        model = InspectionTask
        fields = ('status', 'organization')

    def filter_is_inspector(self, queryset, name, value):  # noqa: WPS110
        if value:
            return queryset.filter(inspector=self.request.user, type=InspectorTaskTypes.FOR_SEARCH_INSPECTOR)
        return queryset

    def filter_is_author(self, queryset, name, value):  # noqa: WPS110
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
