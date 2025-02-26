from django.core.exceptions import FieldError
from django_filters import CharFilter, FilterSet
from rest_framework.exceptions import ValidationError

from apps.notification.models import BaseNotification


def _get_subclasses_as_choice(klass):
    choices = {
        subclass.__name__.lower(): subclass
        for subclass in klass.__subclasses__()
    }
    return choices


class NotificationFilterSet(FilterSet):
    resourcetype = CharFilter(method='filter_by_resourcetype')

    class Meta:
        model = BaseNotification
        fields = ()

    def filter_by_resourcetype(self, queryset, name, value):
        try:  # noqa: WPS229
            event_choices = _get_subclasses_as_choice(BaseNotification)
            selected_events = [v for k, v in event_choices.items() if value.lower() == k]
            return queryset.instance_of(*selected_events)
        except FieldError:
            raise ValidationError({'resourcetype': 'Неверное значение resourcetype'})
