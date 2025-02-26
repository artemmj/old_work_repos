import pytest

from apps.zone.models import Zone
from apps.zone.services.bulk_update_storage_name_zone import BulkUpdateStorageNameZoneService

pytestmark = [pytest.mark.django_db]


def test_bulk_update_storage_name_zone_in_range(project_for_bulk_update_storage_name_zone):
    """Тест для проверки сервиса изменения названий складов зон в диапазоне."""
    project_id = project_for_bulk_update_storage_name_zone.id
    storage_name = 'Тестовый склад'
    start_serial_number = 1
    end_serial_number = 4

    filter_options = {
        'project_id': project_id,
        'serial_number__gte': start_serial_number,
        'serial_number__lte': end_serial_number,
    }

    BulkUpdateStorageNameZoneService().process(filter_options, storage_name)

    assert Zone.objects.get(serial_number=4).storage_name == 'Тестовый склад'
    assert Zone.objects.get(serial_number=5).storage_name != 'Тестовый склад'


def test_bulk_update_storage_name_zone_select(project_for_bulk_update_storage_name_zone):
    """Тест для проверки сервиса изменения названий складов зон выборочно."""
    project_id = project_for_bulk_update_storage_name_zone.id
    storage_name = 'Тестовый склад'
    zone_id_serial_number_1 = Zone.objects.get(serial_number=1).id
    zone_id_serial_number_3 = Zone.objects.get(serial_number=3).id
    zones_ids = [zone_id_serial_number_1, zone_id_serial_number_3]

    filter_options = {
        'project_id': project_id,
        'pk__in': zones_ids,
    }

    BulkUpdateStorageNameZoneService().process(filter_options, storage_name)

    assert Zone.objects.get(serial_number=1).storage_name == 'Тестовый склад'
    assert Zone.objects.get(serial_number=2).storage_name != 'Тестовый склад'
    assert Zone.objects.get(serial_number=3).storage_name == 'Тестовый склад'
