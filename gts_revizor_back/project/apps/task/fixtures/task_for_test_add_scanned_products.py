import pytest
from mixer.backend.django import mixer

from apps.document.models import Document, DocumentStatusChoices, DocumentColorChoices
from apps.product.models import ScannedProduct, Product
from apps.task.models import TaskTypeChoices, TaskStatusChoices, Task
from apps.zone.models import ZoneStatusChoices, Zone

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def task_for_test_add_scanned_products(project):
    """Фикстура задания для проверки сервиса добавления отсканированных товаров в таску."""
    zone = mixer.blend(
        Zone,
        project=project,
        serial_number=1,
        status=ZoneStatusChoices.READY,
    )
    task = mixer.blend(
        Task,
        zone=zone,
        type=TaskTypeChoices.COUNTER_SCAN,
        result=5,
        status=TaskStatusChoices.SUCCESS_SCAN,
    )
    mixer.blend(
        Document,
        zone=zone,
        counter_scan_task=task,
        status=DocumentStatusChoices.READY,
        color=DocumentColorChoices.GREEN,
    )
    product = mixer.blend(
        Product,
        project=project,
        title='Товар',
        barcode='567',
        vendor_code='321',
        qr_code='http://qr_code_2',
    )
    mixer.blend(
        Product,
        project=project,
        title='Весовой',
        barcode='000',
        vendor_code='999',
        qr_code='http://qr_code_3',
    )
    mixer.blend(
        ScannedProduct,
        product=product,
        task=task,
        amount=5,
        is_weight=False,
    )
    return task
