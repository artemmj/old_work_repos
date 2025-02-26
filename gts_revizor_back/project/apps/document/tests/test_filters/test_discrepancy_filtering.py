import pytest
from pytest import fixture
from rest_framework import status
from rest_framework.test import APIClient

from apps.employee.models import Employee
from apps.project.models import Project
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]

ENTITY_COUNT = 5


@pytest.mark.parametrize(
    'filter_value, documents_count_after_filtering',
    [
        ('true', 2),
        ('false', 3),
    ]
)
def test_discrepancy_filtering_successful(
    client: APIClient,
    products_factory: fixture,
    documents_factory: fixture,
    tasks_factory: fixture,
    scanned_products_factory: fixture,
    zone: Zone,
    employee: Employee,
    project: Project,
    filter_value: str,
    documents_count_after_filtering: int,
):
    products = products_factory(count=ENTITY_COUNT, project=project)
    counter_tasks = tasks_factory(count=ENTITY_COUNT, zone=zone, employee=employee)
    auditor_tasks = tasks_factory(count=ENTITY_COUNT, zone=zone, employee=employee)
    scanned_products_factory(
        count=ENTITY_COUNT,
        product=(v for v in products),
        amount=(v for v in [1, 2, 3, 4, 5]),
        task=(v for v in counter_tasks),
    )
    scanned_products_factory(
        count=ENTITY_COUNT,
        product=(v for v in products),
        amount=(v for v in [1, 2, 3, 8, 20]),
        task=(v for v in auditor_tasks),
    )
    documents_factory(
        count=ENTITY_COUNT,
        project=project,
        counter_scan_task=(v for v in counter_tasks),
        auditor_task=(v for v in auditor_tasks),
    )

    url = f'/api/v1/document/?auditor_task__result__discrepancy={filter_value}'
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == documents_count_after_filtering
