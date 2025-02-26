import pytest
from mixer.backend.django import mixer

from apps.document.models import DocumentStatusChoices, DocumentColorChoices
from apps.product.models import Product
from apps.task.models import TaskStatusChoices, TaskTypeChoices
from apps.zone.models import ZoneStatusChoices

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def project_barcode_and_dm_matches_report(
    project,
    products_factory,
    scanned_products_factory,
    documents_factory,
    zones_factory,
    tasks_factory,
):
    """Фикстура создания проекта для отчета Совпадения Шк по Зонам(Датаматрикс по зонам)."""
    zones = zones_factory(
        count=3,
        project=project,
        serial_number=(serial_number for serial_number in [1, 2, 3]),
        status=(status for status in [ZoneStatusChoices.READY, ZoneStatusChoices.NOT_READY, ZoneStatusChoices.READY]),
    )
    tasks = tasks_factory(
        count=3,
        zone=(zone for zone in zones),
        type=(type for type in [TaskTypeChoices.COUNTER_SCAN, TaskTypeChoices.AUDITOR, TaskTypeChoices.COUNTER_SCAN]),
        status=(
            status
            for status in [TaskStatusChoices.SUCCESS_SCAN, TaskStatusChoices.FAILED_SCAN, TaskStatusChoices.WORKED]
        ),
    )
    product = mixer.blend(
        Product,
        project=project,
        title='Test',
        barcode='barcode',
        vendor_code='vendor_code',
    )
    product_with_dm = mixer.blend(
        Product,
        project=project,
        title='Test 2',
        barcode='bar',
        vendor_code='vendor',
        dm='dm2',
    )
    scanned_products_factory(
        count=3,
        product=product,
        task=(task for task in tasks),
        amount=(amount for amount in [1, 1, 1]),
    )
    scanned_products_factory(
        count=3,
        product=product_with_dm,
        task=(task for task in tasks),
        amount=(amount for amount in [1, 1, 1]),
    )
    documents_factory(
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
    return project
