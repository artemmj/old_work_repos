import pytest

from apps.employee.models import EmployeeRoleChoices
from apps.zone.models import ZoneStatusChoices

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def project_for_create_task_and_bulk_create_scanned_products(
    project,
    zones_factory,
    products_factory,
    terminals_factory,
    employee_factory,

):
    """Фикстура создания проекта для сервиса CreateTaskAndBulkCreateScannedProductsService."""
    zones_factory(
        count=1,
        project=project,
        serial_number=1,
        status=ZoneStatusChoices.READY,
    )
    products_factory(
        count=2,
        project=project,
        barcode=(barcode for barcode in ['111', '222']),
    )
    terminals_factory(
        count=1,
        project=project,
        number=99900,
        device_model='MC2200',
    )
    employee_factory(
        count=1,
        project=project,
        username='Сотрудник 1',
        serial_number=1,
        roles=[EmployeeRoleChoices.COUNTER],
        is_deleted=False,
        is_auto_assignment=True,
    )
    return project
