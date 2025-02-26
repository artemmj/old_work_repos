import pytest

from api.v1.document.services.get_documents import GetDocumentsService
from apps.employee.models import Employee
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]


def test_get_documents_successful(
    documents_factory,
    products_factory,
    tasks_factory,
    employee: Employee,
    zone: Zone,
):
    """Тест сервиса получения документов."""
    counter_task = tasks_factory(count=1, zone=zone, employee=employee, result=50)
    controller_task = tasks_factory(count=1, zone=zone, employee=employee, result=45)

    documents_factory(
        count=1,
        employee=employee,
        counter_scan_task=counter_task,
        controller_task=controller_task,
    )

    created_documents = GetDocumentsService().process()
    created_document = created_documents.first()

    assert created_documents.count() == 1
    assert created_document.counter_scan_barcode_amount == 50
    assert created_document.controller_barcode_amount == 45
