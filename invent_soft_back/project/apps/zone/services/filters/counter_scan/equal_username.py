import logging

from django.db.models import QuerySet

from apps.helpers.services import AbstractService
from apps.task.models import TaskTypeChoices

logger = logging.getLogger('django')


class ZoneFilteringByEqCounterScanUsernameService(AbstractService):
    """Сервис фильтрации зон по полному вхождению переданного значения в юзернейм счётчика."""

    def __init__(self, queryset: QuerySet, counter_scan_username: str):
        self.queryset = queryset
        self.counter_scan_username = counter_scan_username

    def process(self, *args, **kwargs):  # noqa: WPS231
        return (
            self.queryset
            .check_is_one_counter_scan_to_zone(value=self.counter_scan_username)
            .filter(
                tasks__employee__username__iexact=self.counter_scan_username,
                tasks__type=TaskTypeChoices.COUNTER_SCAN,
                is_one_counter_scan_to_zone=True,
            )
            .distinct()
        )
