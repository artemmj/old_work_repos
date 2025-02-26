from django_filters import CharFilter, FilterSet

from apps.employee.models import Employee


class EmployeeFilterSet(FilterSet):
    role = CharFilter(method='role_filter')

    class Meta:
        model = Employee
        fields = ('project',)

    def role_filter(self, queryset, name, value):
        if value:
            return queryset.filter(roles__icontains=value)
        return queryset
