import pytest
from mixer.backend.django import mixer

from apps.document.models import Document
from apps.task.models import TaskTypeChoices, TaskStatusChoices
from apps.zone.models import ZoneStatusChoices, Zone

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def document_discrepancy_report(
    project,
    products_factory,
    scanned_products_factory,
    zones_factory,
    tasks_factory,
):
    """Фикстура создания документа для отчета по расхождениям в ходе фискальной инвентаризации"""
    zone = mixer.blend(
        Zone,
        project=project,
        serial_number=1,
        status=ZoneStatusChoices.READY,
    )
    tasks = tasks_factory(
        count=3,
        zone=zone,
        type=TaskTypeChoices.COUNTER_SCAN,
        result=50,
        status=TaskStatusChoices.SUCCESS_SCAN,
    )
    products = products_factory(
        count=3,
        project=project,
        title=(title for title in ['Test', 'Test_2', 'Неизвестный товар']),
        barcode=(barcode for barcode in ['3333', '2222', '1111']),
        vendor_code=(vendor_code for vendor_code in ['9999', '8888', '7777'])
    )
    scanned_products_factory(
        count=3,
        product=(product for product in products),
        task=(task for task in tasks),
        amount=(amount for amount in [20, 16, 18]),
    )
    document = mixer.blend(
        Document,
        serial_number=1,
        zone=zone,
        counter_scan_task=tasks[0],
        auditor_task=tasks[1],
        auditor_external_task=tasks[-1],
    )

    return document
