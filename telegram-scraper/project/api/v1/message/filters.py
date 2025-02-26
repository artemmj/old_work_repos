from django_filters import DateFromToRangeFilter, FilterSet

from apps.message.models import Message


class MessageFilterSet(FilterSet):
    ext_date = DateFromToRangeFilter(field_name='ext_date')

    class Meta:
        model = Message
        fields = ('channel', 'ext_date')
