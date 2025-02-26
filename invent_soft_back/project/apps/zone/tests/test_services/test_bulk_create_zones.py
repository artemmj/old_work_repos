import pytest

from apps.zone.models import Zone
from apps.zone.services import BulkCreateZonesService

pytestmark = [pytest.mark.django_db]


def test_bulk_create_zones(project):
    """Тест для проверки массового создания зон."""
    zones_content = [
        {
            'id': 'de17c51c-9769-414d-87f1-bd976e42cd08',
            'serial_number': 30849,
            'title': '593000',
            'storage_name': '',
            'code': '4-369-01-4-03',
            'status': 'not_ready',
            'is_auto_assignment': True,
        },
        {
            'id': '97a51bf9-5865-4d6b-8ca7-4125f7f3be1e',
            'serial_number': 30848,
            'title': '651607',
            'storage_name': '',
            'code': '4-369-28-4-02',
            'status': 'not_ready',
            'is_auto_assignment': True,
        },
    ]

    BulkCreateZonesService(project, zones_content).process()

    assert Zone.objects.filter(project=project).count() == 2
