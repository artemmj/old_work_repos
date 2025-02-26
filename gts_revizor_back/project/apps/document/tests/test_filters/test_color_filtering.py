import pytest
from pytest import fixture
from rest_framework import status
from rest_framework.test import APIClient

from apps.employee.models import Employee
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]

ENTITY_COUNT = 5


@pytest.mark.parametrize(
    'filter_value, documents_count_after_filtering',
    [
        ('red, green', 4),
        ('red, white', 4),
        ('green, white', 2),
        ('green, white, red', 5),
    ]
)
def test_color_filtering_successful(
    client: APIClient,
    documents_factory: fixture,
    tasks_factory: fixture,
    zone: Zone,
    employee: Employee,
    filter_value: str,
    documents_count_after_filtering: int,
):
    colors = ['red', 'white', 'red', 'green', 'red']

    counter_tasks = tasks_factory(count=ENTITY_COUNT, zone=zone, employee=employee)
    auditor_tasks = tasks_factory(count=ENTITY_COUNT, zone=zone, employee=employee)

    documents_factory(
        count=ENTITY_COUNT,
        project=zone.project,
        zone=zone,
        counter_scan_task=(v for v in counter_tasks),
        auditor_task=(v for v in auditor_tasks),
        color=(color for color in colors)
    )

    url = f'/api/v1/document/?project={zone.project.id}&colors={filter_value}'
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == documents_count_after_filtering
