import pytest

from apps.task.models import TaskTypeChoices
from apps.zone.models import ZoneStatusChoices

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def project_for_bulk_create_scanned_products(
    project,
    zones_factory,
    tasks_factory,
    products_factory,
):
    """Фикстура создания проекта для сервиса BulkCreateScannedProductsService."""
    zone = zones_factory(
        count=1,
        project=project,
        serial_number=1,
        status=ZoneStatusChoices.READY,
    )
    tasks_factory(
        count=1,
        zone=zone,
        type=TaskTypeChoices.COUNTER_SCAN,
    )
    products_factory(
        count=2,
        project=project,
        barcode=(barcode for barcode in ['111', '222']),
    )

    return project
