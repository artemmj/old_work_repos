import pytest

from apps.employee.models import EmployeeRoleChoices
from apps.project.models import Project
from apps.task.models import TaskTypeChoices, TaskStatusChoices
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]


def test_get_counter_scans_usernames_in_zone_successful(
    project: Project,
    tasks_factory,
    zones_factory,
    employee_factory,
):
    """Тест для проверки получения юзернеймов счётчиков зоны."""
    zone = zones_factory(count=1, project=project)
    counter_scan = employee_factory(
        count=1,
        project=project,
        username='Сотрудник 1',
        roles=[EmployeeRoleChoices.COUNTER],
    )

    tasks_factory(
        count=2,
        zone=zone,
        employee=counter_scan,
        type=TaskTypeChoices.COUNTER_SCAN,
        status=(status for status in [TaskStatusChoices.SUCCESS_SCAN, TaskStatusChoices.FAILED_SCAN]),
        result=45,
    )

    created_zone = Zone.objects.with_usernames_of_counter_scans().first()

    assert created_zone.counter_scans == ['Сотрудник 1', 'Сотрудник 1']


def test_get_controllers_usernames_in_zone_successful(
    project: Project,
    tasks_factory,
    zones_factory,
    employee_factory,
):
    """Тест для проверки получения юзернеймов ук зоны."""
    zone = zones_factory(count=1, project=project)
    controller = employee_factory(
        count=1,
        project=project,
        username='Сотрудник 2',
        roles=[EmployeeRoleChoices.COUNTER],
    )

    tasks_factory(
        count=2,
        zone=zone,
        employee=controller,
        type=TaskTypeChoices.CONTROLLER,
        status=(status for status in [TaskStatusChoices.SUCCESS_SCAN, TaskStatusChoices.FAILED_SCAN]),
        result=45,
    )

    created_zone = Zone.objects.with_usernames_of_controllers().first()

    assert created_zone.controllers == ['Сотрудник 2', 'Сотрудник 2']
