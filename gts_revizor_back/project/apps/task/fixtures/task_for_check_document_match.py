import pytest
from mixer.backend.django import mixer

from apps.document.models import DocumentStatusChoices, DocumentColorChoices
from apps.employee.models import Employee, EmployeeRoleChoices
from apps.task.models import TaskTypeChoices, TaskStatusChoices
from apps.terminal.models import Terminal
from apps.zone.models import ZoneStatusChoices, Zone

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def tasks_for_check_documents_match_if_equal_result(
    project,
    tasks_factory,
    documents_factory,
):
    """
    Фикстура создания заданий для проверки функции _assign_if_fail при условии,
    что равны результаты counter_scan_task и db_task.
    """
    zone = mixer.blend(
        Zone,
        project=project,
        serial_number=1,
        status=ZoneStatusChoices.READY,
    )
    employee = mixer.blend(
        Employee,
        project=project,
        roles=[EmployeeRoleChoices.COUNTER],
        serial_number=1,
        is_auto_assignment=True,
    )
    tasks = tasks_factory(
        count=2,
        zone=zone,
        employee=employee,
        result=187,
        type=(type for type in [TaskTypeChoices.CONTROLLER, TaskTypeChoices.COUNTER_SCAN]),
        status=(status for status in [
            TaskStatusChoices.SUCCESS_SCAN,
            TaskStatusChoices.INITIALIZED,
        ]
            ),
    )
    documents_factory(
        count=2,
        zone=zone,
        counter_scan_task=tasks[-1],
        status=(status for status in [DocumentStatusChoices.READY, DocumentStatusChoices.READY]),
        color=(color for color in [DocumentColorChoices.GREEN, DocumentColorChoices.GREEN]),
    )
    mixer.blend(
        Terminal,
        project=project,
        employee=employee,
        number=99900,
        device_model='MC2200',
    )
    return tasks


@pytest.fixture()
def tasks_for_check_documents_match_if_not_equal_result(
    project,
    tasks_factory,
    documents_factory,
):
    """
    Фикстура создания заданий для проверки функции _assign_if_fail при условии,
    что результаты  counter_scan_task и db_task не равны.
    """
    zone = mixer.blend(
        Zone,
        project=project,
        serial_number=1,
        status=ZoneStatusChoices.READY,
    )
    employee = mixer.blend(
        Employee,
        project=project,
        roles=[EmployeeRoleChoices.COUNTER],
        serial_number=1,
        is_auto_assignment=True,
    )
    tasks = tasks_factory(
        count=2,
        zone=zone,
        employee=employee,
        result=(result for result in [187, 190]),
        type=(type for type in [TaskTypeChoices.CONTROLLER, TaskTypeChoices.COUNTER_SCAN]),
        status=(status for status in [
            TaskStatusChoices.SUCCESS_SCAN,
            TaskStatusChoices.INITIALIZED,
        ]
            ),
    )
    documents_factory(
        count=2,
        zone=zone,
        counter_scan_task=tasks[-1],
        status=(status for status in [DocumentStatusChoices.READY, DocumentStatusChoices.READY]),
        color=(color for color in [DocumentColorChoices.GREEN, DocumentColorChoices.GREEN]),
    )
    mixer.blend(
        Terminal,
        project=project,
        employee=employee,
        number=99900,
        device_model='MC2200',
    )
    return tasks
