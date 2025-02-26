import random

import pytest

from api.v1.document.services.replace_specification import ReplaceDocumentSpecificationService
from apps.document.asserts import assert_correct_specification_changing_for
from apps.employee.models import Employee
from apps.project.models import Project
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]


def test_test_replace_specification_successful(
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
    counter_task = tasks_factory(count=1, zone=zone, employee=employee)
    auditor_task = tasks_factory(count=1, zone=zone, employee=employee)
    scanned_products_factory(
        count=5,
        product=(v for v in products),
        amount=(v for v in random.sample(range(1, 50), 5)),
        task=counter_task,
    )
    scanned_products_factory(
        count=5,
        product=(v for v in products),
        amount=(v for v in random.sample(range(1, 50), 5)),
        task=auditor_task,
    )
    document = documents_factory(
        count=1,
        employee=employee,
        counter_scan_task=counter_task,
        auditor_task=auditor_task,
    )

    ReplaceDocumentSpecificationService().process(source='auditor', document=document)

    assert_correct_specification_changing_for(document)
