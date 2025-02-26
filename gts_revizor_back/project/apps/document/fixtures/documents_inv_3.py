import pytest

from apps.document.models import DocumentColorChoices, DocumentStatusChoices
from apps.task.models import TaskStatusChoices, TaskTypeChoices
from apps.zone.models import ZoneStatusChoices

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def documents_inv_three_report(
    project,
    products_factory,
    scanned_products_factory,
    documents_factory,
    zones_factory,
    tasks_factory,
):
    """Фикстура создания документов для отчета ИНВ-3."""
    zones = zones_factory(
        count=3,
        project=project,
        serial_number=(serial_number for serial_number in [1, 2, 3]),
        status=(status for status in [ZoneStatusChoices.READY, ZoneStatusChoices.NOT_READY, ZoneStatusChoices.READY]),
    )
    tasks = tasks_factory(
        count=3,
        zone=(zone for zone in zones),
        type=TaskTypeChoices.COUNTER_SCAN,
        status=TaskStatusChoices.SUCCESS_SCAN,
    )
    documents = documents_factory(
        count=3,
        zone=(zone for zone in zones),
        serial_number=(number for number in [1, 2, 3]),
        counter_scan_task=(task for task in tasks),
        status=(
            status
            for status
            in [DocumentStatusChoices.READY, DocumentStatusChoices.NOT_READY, DocumentStatusChoices.READY]
        ),
        color=(color for color in [DocumentColorChoices.GREEN, DocumentColorChoices.RED, DocumentColorChoices.GREEN]),
    )
    products_unidentified = products_factory(
        count=5,
        project=project,
        title='Неизвестный товар',
        price=100.0,
        barcode='barcode',
        vendor_code='vendor_code',
    )
    products_identified = products_factory(
        count=5,
        project=project,
        price=100.0,
        title='Test',
        barcode='barcode',
        vendor_code='vendor_code',
    )
    scanned_products_factory(
        count=5,
        product=(product for product in products_identified),
        amount=(amount for amount in [3, 5, 2, 1, 9]),
        task=tasks[0],
        added_by_product_code=True,
    )
    scanned_products_factory(
        count=5,
        product=(product for product in products_unidentified),
        amount=(amount for amount in [1, 1, 1, 1, 1]),
        task=tasks[1],
        added_by_product_code=True,
    )
    scanned_products_factory(
        count=5,
        product=(product for product in products_unidentified),
        amount=(amount for amount in [5, 5, 5, 5, 5]),
        task=tasks[-1],
        added_by_product_code=False,
    )
    return documents
