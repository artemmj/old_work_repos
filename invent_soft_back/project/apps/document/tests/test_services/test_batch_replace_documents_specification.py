import random

import pytest

from api.v1.document.services.batch_replace_documents_specification import BatchReplaceDocumentSpecificationService
from apps.document.asserts import assert_correct_specification_changing_for
from apps.employee.models import Employee
from apps.project.models import Project
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]


def test_batch_replace_documents_specification_successful(
    documents_factory,
    products_factory,
    tasks_factory,
    scanned_products_factory,
    employee: Employee,
    project: Project,
    zone: Zone,
):
    """Тест сервиса замены спецификации в документе."""
    products = products_factory(count=5, project=project)
    counter_tasks = tasks_factory(count=5, zone=zone, employee=employee)
    auditor_tasks = tasks_factory(count=5, zone=zone, employee=employee)

    for counter_task in counter_tasks:
        scanned_products_factory(
            count=5,
            product=(product for product in products),
            amount=(product for product in random.sample(range(1, 50), 5)),
            task=counter_task,
        )

    for auditor_task in auditor_tasks:
        scanned_products_factory(
            count=5,
            product=(product for product in products),
            amount=(amount for amount in random.sample(range(1, 50), 5)),
            task=auditor_task,
        )
    documents = documents_factory(
        count=5,
        employee=employee,
        counter_scan_task=(counter_task for counter_task in counter_tasks),
        auditor_task=(auditor_task for auditor_task in auditor_tasks),
    )

    document_ids = [document.id for document in documents]
    updated_documents = BatchReplaceDocumentSpecificationService(document_ids=document_ids, source='auditor').process()

    for document in updated_documents:
        assert_correct_specification_changing_for(document)
