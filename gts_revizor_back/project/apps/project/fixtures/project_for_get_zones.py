import pytest

from apps.task.models import TaskStatusChoices, TaskTypeChoices

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def project_for_get_zones(
    project,
    zones_factory,
    tasks_factory,
    products_factory,
    scanned_products_factory,
):
    zone = zones_factory(count=1, project=project)
    tasks = tasks_factory(
        count=3,
        zone=zone,
        type=(type for type in
              [TaskTypeChoices.COUNTER_SCAN, TaskTypeChoices.COUNTER_SCAN, TaskTypeChoices.CONTROLLER]
              ),
        status=(status for status in
                [TaskStatusChoices.SUCCESS_SCAN, TaskStatusChoices.INITIALIZED, TaskStatusChoices.SUCCESS_SCAN]
                ),
        result=45,
    )
    products = products_factory(
        count=1,
        project=project,
    )
    scanned_products_factory(
        count=2,
        product=products,
        task=tasks[0],
    )
    scanned_products_factory(
        count=3,
        product=products,
        task=tasks[1],
    )

    return project
