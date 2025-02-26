import pytest

from apps.zone.models import Zone
from apps.zone.services.filters.counter_scan.not_equal_username import FilterZoneByNotEqCounterScanUsernameService

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize('counter_scan_username', ['Сотрудник 1', 'сотрудник 1'])
def test_zone_filtering_by_not_eq_counter_scan_username_successful(
    counter_scan_username: str,
    zones_for_testing_filters,
):
    """Тест для проверки фильтрации зон по полному отсутствию юзернейма счётчика."""
    filtering_zone = FilterZoneByNotEqCounterScanUsernameService(
        queryset=Zone.objects.all(),
        counter_scan_username=counter_scan_username,
    ).process()

    assert filtering_zone.count() == 1
