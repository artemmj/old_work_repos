from django_filters import DateTimeFromToRangeFilter, FilterSet

from apps.changelog.models import ChangeLog


class ChangeLogFilterSet(FilterSet):
    created_at = DateTimeFromToRangeFilter()

    class Meta:
        model = ChangeLog
        fields = ('project', 'created_at', 'model', 'action_on_model')
