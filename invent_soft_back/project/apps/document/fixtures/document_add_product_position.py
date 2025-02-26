import pytest
from mixer.backend.django import mixer

from apps.document.models import DocumentStatusChoices, DocumentColorChoices, Document
from apps.product.models import ScannedProduct
from apps.task.models import TaskTypeChoices, TaskStatusChoices, Task
from apps.zone.models import ZoneStatusChoices, Zone

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def document_for_add_product_position(
    project,
    products_factory,
):
    """Фикстура создания документа для проверки сервиса добавления товара в документе."""
    zone = mixer.blend(
        Zone,
        project=project,
        serial_number=1,
        status=ZoneStatusChoices.NOT_READY,
    )
    counter_scan_task = mixer.blend(
        Task,
        zone=zone,
        type=TaskTypeChoices.COUNTER_SCAN,
        status=TaskStatusChoices.FAILED_SCAN,
    )
    products = products_factory(
        count=3,
        project=project,
        title=(title for title in ['Test', 'Test_2', 'Неизвестный товар']),
        barcode=(barcode for barcode in ['3333', '2222', '1111']),
        vendor_code=(vendor_code for vendor_code in ['9999', '8888', '7777'])
    )
    mixer.blend(
        ScannedProduct,
        product=products[0],
        task=counter_scan_task,
        amount=1,
    )
    document = mixer.blend(
        Document,
        zone=zone,
        serial_number=1,
        counter_scan_task=counter_scan_task,
        status=DocumentStatusChoices.NOT_READY,
        color=DocumentColorChoices.RED,
    )
    return document
