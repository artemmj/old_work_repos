from django_filters import CharFilter, FilterSet

from apps.task.models import Task


class TaskFilterSet(FilterSet):
    employee = CharFilter(field_name='employee', required=False)
    zone = CharFilter(field_name='zone', required=False)

    class Meta:
        model = Task
        fields = ('employee', 'zone')
