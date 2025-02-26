from django_filters import CharFilter, FilterSet

from apps.event.models import Event


class EventFilterSet(FilterSet):
    class Meta:
        model = Event
        fields = ('project',)
