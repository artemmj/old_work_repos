import pytest

from apps.document.models import DocumentStatusChoices, DocumentColorChoices
from apps.task.models import TaskStatusChoices, TaskTypeChoices
from apps.zone.models import ZoneStatusChoices

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def project_for_disc_accounting_quantity_report(
    project,
    products_factory,
    scanned_products_factory,
    documents_factory,
    zones_factory,
    tasks_factory,
):
    """Фикстура создания проекта для отчета Расхождение с учетным количеством."""
    zones = zones_factory(
        count=3,
        project=project,
        serial_number=(serial_number for serial_number in [1, 2, 3]),
        status=(status for status in [ZoneStatusChoices.READY, ZoneStatusChoices.NOT_READY, ZoneStatusChoices.READY]),
    )
    counter_scan_tasks = tasks_factory(
        count=3,
        zone=(zone for zone in zones),
        type=TaskTypeChoices.COUNTER_SCAN,
        result=50,
        status=TaskStatusChoices.SUCCESS_SCAN,
    )
    products = products_factory(
        count=3,
        project=project,
        price=float(500),
        remainder=3,
        barcode=(barcode for barcode in ['333', '444', '555']),
        vendor_code=(vendor_code for vendor_code in ['222', '111', '000']),
    )
    scanned_products_factory(
        count=3,
        product=(product for product in products),
        task=(task for task in counter_scan_tasks),
        amount=(amount for amount in [2, 1, 9])
    )
    documents_factory(
        count=3,
        zone=(zone for zone in zones),
        serial_number=(number for number in [1, 2, 3]),
        counter_scan_task=(task for task in counter_scan_tasks),
        status=(
            status
            for status
            in [DocumentStatusChoices.READY, DocumentStatusChoices.NOT_READY, DocumentStatusChoices.READY]
        ),
        color=(color for color in [DocumentColorChoices.GREEN, DocumentColorChoices.RED, DocumentColorChoices.GREEN]),
    )

    return project
