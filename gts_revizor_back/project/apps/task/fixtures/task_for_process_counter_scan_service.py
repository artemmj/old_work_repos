import pytest
from mixer.backend.django import mixer

from apps.document.models import DocumentStatusChoices, DocumentColorChoices
from apps.employee.models import Employee, EmployeeRoleChoices
from apps.task.models import TaskTypeChoices, TaskStatusChoices
from apps.terminal.models import Terminal
from apps.zone.models import ZoneStatusChoices, Zone

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def task_for_process_counter_scan(
    project,
    tasks_factory,
    documents_factory,
):
    """
    Фикстура создания тасок для проверки сервиса ProcessCounterScanService .
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
    auditors_tasks = tasks_factory(
        count=3,
        zone=zone,
        employee=employee,
        result=187,
        type=(type for type in [
            TaskTypeChoices.AUDITOR,
            TaskTypeChoices.AUDITOR_EXTERNAL,
            TaskTypeChoices.AUDITOR_CONTROLLER,
        ]),
        status=TaskStatusChoices.SUCCESS_SCAN,
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
        status=(status for status in [
            DocumentStatusChoices.READY,
            DocumentStatusChoices.READY,
        ]),
        color=(color for color in [
            DocumentColorChoices.GREEN,
            DocumentColorChoices.GREEN,
        ]),
        is_replace_specification=True,
    )
    mixer.blend(
        Terminal,
        project=project,
        employee=employee,
        number=99900,
        device_model='MC2200',
    )
    return tasks
