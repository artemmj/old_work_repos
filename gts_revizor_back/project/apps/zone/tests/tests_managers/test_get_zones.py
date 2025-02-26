import pytest

from apps.zone.managers import ZoneManager
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]


def test_get_zones(project_for_get_zones):
    """Тест для проверки получения зон с доп атрибутами."""
    zones = Zone.objects.all()

    zones_with_virtual_attrs = ZoneManager().get_zones(zones)
    zone_with_virtual_attrs = zones_with_virtual_attrs.first()

    assert zone_with_virtual_attrs.barcode_amount == 45
    assert zone_with_virtual_attrs.tasks_scanned_products_count == 2
    assert len(zone_with_virtual_attrs.counter_scan_tasks) == 2
    assert len(zone_with_virtual_attrs.counter_scan_tasks_status) == 1
