import pytest

from apps.project.models import Project
from apps.zone.models import Zone
from apps.zone.services.bulk_create import BulkCreateZoneService

pytestmark = [pytest.mark.django_db]


def test_bulk_create_zones_successful(project: Project):
    """Тест для успешного пакетного создания зон."""
    BulkCreateZoneService(
        project=project,
        storage_name='Склад',
        start_serial_number=1,
        end_serial_number=11,
        batch_size=5,
    ).process()

    created_zones = Zone.objects.all()
    assert created_zones.count() == 10
