import pytest
from mixer.backend.django import mixer

from apps.document.models import DocumentStatusChoices, Document
from apps.employee.models import Employee, EmployeeRoleChoices
from apps.task.models import TaskTypeChoices, TaskStatusChoices
from apps.terminal.models import Terminal
from apps.zone.models import ZoneStatusChoices, Zone

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def tasks_for_make_batch_tasks_counter_scan(
    project,
    tasks_factory,
):
    """ Фикстура создания заданий для проверки функции _make_batch_tasks_counter_scan сервиса CheckAutoAssignService"""
    zone = mixer.blend(
        Zone,
        project=project,
        serial_number=1,
        status=ZoneStatusChoices.READY,
        is_auto_assignment=True
    )
    mixer.blend(
        Zone,
        project=project,
        serial_number=2,
        status=ZoneStatusChoices.NOT_READY,
        is_auto_assignment=True,
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
        status=TaskStatusChoices.SUCCESS_SCAN,
    )
    mixer.blend(
        Document,
        zone=zone,
        counter_scan_task=tasks[0],
        status=DocumentStatusChoices.READY,
    )
    mixer.blend(
        Terminal,
        project=project,
        employee=employee,
        number=99900,
        device_model='MC2200',
    )
    return tasks
