import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.employee.models import Employee
from apps.task.models import TaskTypeChoices
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize(
    'filtering_argument, filter_value, documents_count_after_filtering',
    [
        ('counter_scan_barcode_amount_eq', 0, 2),
        ('counter_scan_barcode_amount_eq', 30, 2),
        ('counter_scan_barcode_amount_not_eq', 0, 8),
        ('counter_scan_barcode_amount_not_eq', 30, 8),
        ('counter_scan_barcode_amount_more_than', 0, 10),
        ('counter_scan_barcode_amount_more_than', 30, 7),
        ('counter_scan_barcode_amount_less_than', 0, 2),
        ('counter_scan_barcode_amount_less_than', 6, 3),

        ('controller_barcode_amount_eq', 0, 2),
        ('controller_barcode_amount_eq', 30, 2),
        ('controller_barcode_amount_not_eq', 0, 8),
        ('controller_barcode_amount_not_eq', 30, 8),
        ('controller_barcode_amount_more_than', 0, 10),
        ('controller_barcode_amount_more_than', 30, 7),
        ('controller_barcode_amount_less_than', 0, 2),
        ('controller_barcode_amount_less_than', 6, 3),
    ]
)
def test_filtering_by_scanned_products_successful(
    client: APIClient,
    documents_factory,
    zone: Zone,
    filtering_argument,
    filter_value: int,
    documents_count_after_filtering: int,
    employee: Employee,
    tasks_factory,
):
    """Тестирование успешной фильтрации документов по количеству ШК.

    Для:
       - скана;
       - УК;

    Args:
        client: API клиент DRF
        documents_factory: фабрика для наполнения БД документами
        zone: фикстура зоны;
        filtering_argument: аргумент фильтрации в URL
        filter_value: значение поля, по которому делается фильтрация
        documents_count_after_filtering: количество документов после фильтрации по переданному полю
    """
    counter_scan_tasks = tasks_factory(
        count=10,
        zone=zone,
        employee=employee,
        type=TaskTypeChoices.COUNTER_SCAN,
        result=(amount for amount in [5, 0, 0, 30, 30, 55, 89, 103, 103, 44])
    )
    controller_tasks = tasks_factory(
        count=10,
        zone=zone,
        employee=employee,
        type=TaskTypeChoices.CONTROLLER,
        result=(amount for amount in [5, 0, 0, 30, 30, 55, 89, 103, 103, 44])
    )

    documents_factory(
        count=10,
        project=zone.project,
        zone=zone,
        counter_scan_task=(v for v in counter_scan_tasks),
        controller_task=(v for v in controller_tasks),
    )

    url = f'/api/v1/document/?project={zone.project.id}&{filtering_argument}={filter_value}'
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == documents_count_after_filtering
