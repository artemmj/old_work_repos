import pytest
from mixer.backend.django import mixer

from apps.employee.models import Employee, EmployeeRoleChoices
from apps.project.models import Project
from apps.task.models import TaskTypeChoices, TaskStatusChoices
from apps.zone.models import Zone, ZoneStatusChoices

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def project_for_auto_assignment(
    tasks_factory,
    employee: Employee,
):
    project = mixer.blend(Project)

    zones = mixer.cycle(5).blend(
        Zone,
        project=project,
        status=(
            status
            for status
            in [
                ZoneStatusChoices.NOT_READY,
                ZoneStatusChoices.NOT_READY,
                ZoneStatusChoices.READY,
                ZoneStatusChoices.READY,
                ZoneStatusChoices.NOT_READY,
            ]
        ),
        is_auto_assignment=(
            is_auto_assignment
            for is_auto_assignment
            in [True, True, False, False, True]
        ),
    )

    for zone in zones:
        tasks_factory(
            count=5,
            zone=zone,
            employee=employee,
            type=(task_type for task_type in [
                TaskTypeChoices.AUDITOR,
                TaskTypeChoices.AUDITOR,
                TaskTypeChoices.AUDITOR,
                TaskTypeChoices.CONTROLLER,
                TaskTypeChoices.CONTROLLER,
            ]
            ),
        )

    employees = mixer.cycle(5).blend(
        Employee,
        project=project,
        roles=[EmployeeRoleChoices.COUNTER],
        serial_number=(number for number in [5, 3, 1, 9, 7]),
        is_auto_assignment=(is_auto_assignment for is_auto_assignment in [True, True, False, False, True]),
    )

    for employee in employees[:2]:
        tasks_factory(
            count=3,
            employee=employee,
            type=(
                task_type
                for task_type
                in [
                    TaskTypeChoices.AUDITOR,
                    TaskTypeChoices.CONTROLLER,
                    TaskTypeChoices.COUNTER_SCAN,
                ]
            ),
            status=(
                status
                for status
                in [
                    TaskStatusChoices.INITIALIZED,
                    TaskStatusChoices.INITIALIZED,
                    TaskStatusChoices.WORKED,
                ]
            ),
        )

    for employee in employees[2:]:
        tasks_factory(
            count=5,
            employee=employee,
            type=(
                task_type
                for task_type
                in [
                    TaskTypeChoices.AUDITOR_EXTERNAL,
                    TaskTypeChoices.AUDITOR,
                    TaskTypeChoices.AUDITOR_EXTERNAL,
                    TaskTypeChoices.CONTROLLER,
                    TaskTypeChoices.CONTROLLER,
                ]
            ),
            status=(
                status
                for status
                in [
                    TaskStatusChoices.INITIALIZED,
                    TaskStatusChoices.INITIALIZED,
                    TaskStatusChoices.WORKED,
                    TaskStatusChoices.FAILED_SCAN,
                    TaskStatusChoices.SUCCESS_SCAN,
                ]
            ),
        )

    return project
