import pytest

from apps.zone.models import Zone
from apps.zone.services.filters.counter_scan.equal_username import ZoneFilteringByEqCounterScanUsernameService

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize('counter_scan_username', ['Сотрудник 1', 'сотрудник 1'])
def test_zone_filtering_by_eq_counter_scan_username_successful(
    counter_scan_username: str,
    zones_for_testing_filters,
):
    """Тест для проверки фильтрации зон по полному вхождению юзернейма счётчика."""
    filtering_zone = ZoneFilteringByEqCounterScanUsernameService(
        queryset=Zone.objects.all(),
        counter_scan_username=counter_scan_username,
    ).process()

    assert len(filtering_zone) == 2
