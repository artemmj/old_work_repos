import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.project.models import Project
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize(
    'filtering_task_field, filter_condition, filter_value, documents_count_after_filtering',
    [
        ('counter_scan_task__result', 'eq', 0, 2),
        ('counter_scan_task__result', 'eq', 2, 1),
        ('counter_scan_task__result', 'not_eq', 0, 3),
        ('counter_scan_task__result', 'not_eq', 2, 4),
        ('counter_scan_task__result', 'more_than', 0, 5),
        ('counter_scan_task__result', 'more_than', 2, 3),
        ('counter_scan_task__result', 'less_than', 0, 2),
        ('counter_scan_task__result', 'less_than', 5, 4),

        ('controller_task__result', 'eq', 0, 2),
        ('controller_task__result', 'eq', 2, 1),
        ('controller_task__result', 'not_eq', 0, 3),
        ('controller_task__result', 'not_eq', 2, 4),
        ('controller_task__result', 'more_than', 0, 5),
        ('controller_task__result', 'more_than', 2, 3),
        ('controller_task__result', 'less_than', 0, 2),
        ('controller_task__result', 'less_than', 5, 4),

        ('auditor_task__result', 'eq', 0, 2),
        ('auditor_task__result', 'eq', 2, 1),
        ('auditor_task__result', 'not_eq', 0, 3),
        ('auditor_task__result', 'not_eq', 2, 4),
        ('auditor_task__result', 'contains', 0, 3),
        ('auditor_task__result', 'not_contains', 0, 2),

        ('auditor_controller_task__result', 'eq', 0, 2),
        ('auditor_controller_task__result', 'eq', 2, 1),
        ('auditor_controller_task__result', 'not_eq', 0, 3),
        ('auditor_controller_task__result', 'not_eq', 2, 4),
        ('auditor_controller_task__result', 'contains', 0, 3),
        ('auditor_controller_task__result', 'not_contains', 0, 2),
    ]
)
def test_filtering_by_scanned_products_successful(
    client: APIClient,
    documents_factory,
    project: Project,
    zone: Zone,
    filtering_task_field: str,
    filter_condition: str,
    filter_value: int,
    documents_count_after_filtering: int,
):
    """Тестирование успешной фильтрации по отсканированным продуктам.

    Для:
       - скана;
       - УК;
       - аудитора;
       - аудитора УК.

    Args:
        client: API клиент DRF
        documents_factory: фабрика для наполнения БД документами
        project: фикстура проекта
        zone: фикстура зоны;
        filtering_task_field: поле, по которому делается фильтрация
        filter_condition: условие фильтрации (больше, меньше, содержит, не содержит и т.д.)
        filter_value: значение поля, по которому делается фильтрация
        documents_count_after_filtering: количество документов после фильтрации по переданному полю
    """
    documents_factory(
        count=5,
        **{
            'project': project,
            'zone': zone,
            f'{filtering_task_field}': (v for v in [0, 0, 5, 2, 10]),
        },
    )
    documents_factory(
        count=5,
        project=project,
        zone=zone,
    )

    url = f'/api/v1/document/?project={project.id}&{filtering_task_field}_{filter_condition}={filter_value}'
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == documents_count_after_filtering
