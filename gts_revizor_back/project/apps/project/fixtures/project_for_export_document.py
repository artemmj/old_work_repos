import pytest

from apps.document.models import DocumentColorChoices, DocumentStatusChoices
from apps.task.models import TaskStatusChoices, TaskTypeChoices
from apps.zone.models import ZoneStatusChoices

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def project_for_export_document(
    project,
    products_factory,
    scanned_products_factory,
    documents_factory,
    zones_factory,
    tasks_factory,
):
    zones = zones_factory(
        count=3,
        project=project,
        title=(title for title in ['zone_1', 'zone_2', 'zone_3']),
        serial_number=(serial_number for serial_number in [1, 2, 3]),
        status=(status for status in [ZoneStatusChoices.READY, ZoneStatusChoices.NOT_READY, ZoneStatusChoices.READY]),
    )
    counter_scan_tasks = tasks_factory(
        count=3,
        zone=(zone for zone in zones),
        type=TaskTypeChoices.COUNTER_SCAN,
        result=(result for result in [9, 0, 35]),
        status=TaskStatusChoices.SUCCESS_SCAN,
    )
    products = products_factory(
        count=3,
        project=project,
        title=(title for title in ['Первый', 'Второй', 'Неизвестный']),
        price=float(500),
        remainder=(rem for rem in [10, 20, 30]),
        remainder_2=None,
        barcode=(barcode for barcode in ['1111', '2222', '3333']),
        vendor_code=(vendor_code for vendor_code in ['qqq', 'www', 'eee'])
    )
    scanned_products_factory(
        count=3,
        product=(product for product in products),
        task=(task for task in counter_scan_tasks),
        amount=(amount for amount in [9, 0, 35]),
        added_by_product_code=(added_by_product_code for added_by_product_code in [True, True, False]),
    )
    documents_factory(
        count=3,
        zone=(zone for zone in zones),
        counter_scan_task=(task for task in counter_scan_tasks),
        status=(
            status for status in [DocumentStatusChoices.READY, DocumentStatusChoices.READY, DocumentStatusChoices.READY]
        ),
        color=(color for color in [DocumentColorChoices.GREEN, DocumentColorChoices.GREEN, DocumentColorChoices.GREEN]),
    )
    return project
