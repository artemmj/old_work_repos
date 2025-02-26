from django_filters import FilterSet, UUIDFilter

from apps.terminal.models import Terminal


class TerminalFilterSet(FilterSet):
    project = UUIDFilter(field_name='project', required=True)

    class Meta:
        model = Terminal
        fields = ('project',)
