import pytest

from apps.project.models import Project
from apps.task.models import TaskTypeChoices, TaskStatusChoices
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]


def test_calculate_tasks_scanned_products_count_in_zone_successful(
    project: Project,
    tasks_factory,
    zones_factory,
    products_factory,
    scanned_products_factory,
):
    """Тест для проверки расчёта количества отсканированных продуктов в зоне."""
    zone_with_zero_scanned_products = zones_factory(count=1, project=project)
    zone_with_non_zero_scanned_products = zones_factory(count=1, project=project)

    tasks_factory(
        count=2,
        zone=zone_with_zero_scanned_products,
        type=TaskTypeChoices.COUNTER_SCAN,
        status=(status for status in [TaskStatusChoices.SUCCESS_SCAN, TaskStatusChoices.FAILED_SCAN]),
        result=45,
    )

    tasks_with_scanned_products = tasks_factory(
        count=2,
        zone=zone_with_non_zero_scanned_products,
        type=TaskTypeChoices.COUNTER_SCAN,
        status=(status for status in [TaskStatusChoices.SUCCESS_SCAN, TaskStatusChoices.FAILED_SCAN]),
        result=45,
    )

    products = products_factory(
        count=2,
        project=project,
    )

    scanned_products = scanned_products_factory(
        count=2,
        product=(product for product in products),
        task=(task for task in tasks_with_scanned_products),
        amount=(amount for amount in [1, 2]),
    )

    created_zone_with_zero_scanned_products = Zone.objects.calculate_tasks_scanned_products_count().first()

    assert created_zone_with_zero_scanned_products.tasks_scanned_products_count == len(scanned_products)
