import logging

from django.db.models import QuerySet

from apps.helpers.services import AbstractService
from apps.task.models import TaskTypeChoices

logger = logging.getLogger('django')


class FilterZoneByNotEqCounterScanUsernameService(AbstractService):
    """Сервис фильтрации зон по полному отсутствию переданного значения в юзернейм счётчика."""

    def __init__(self, queryset: QuerySet, counter_scan_username: str):
        self.queryset = queryset
        self.counter_scan_username = counter_scan_username

    def process(self, *args, **kwargs):
        return (
            self.queryset
            .exclude(
                tasks__employee__username__iexact=self.counter_scan_username,
                tasks__type=TaskTypeChoices.COUNTER_SCAN,
            )
            .distinct()
        )
