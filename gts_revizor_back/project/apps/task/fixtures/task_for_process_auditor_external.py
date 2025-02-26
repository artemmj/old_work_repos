import pytest
from mixer.backend.django import mixer

from apps.document.models import DocumentStatusChoices, Document
from apps.employee.models import Employee, EmployeeRoleChoices
from apps.task.models import TaskTypeChoices, TaskStatusChoices, Task
from apps.terminal.models import Terminal
from apps.zone.models import ZoneStatusChoices, Zone

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def task_for_process_auditor_external(project):
    """Фикстура создания задания для проверки cервиса обработки задания ВНЕШНИЙ АУДИТОР."""
    zone = mixer.blend(
        Zone,
        project=project,
        serial_number=1,
        status=ZoneStatusChoices.READY,
    )
    task = mixer.blend(
        Task,
        zone=zone,
        type=TaskTypeChoices.COUNTER_SCAN,
        status=TaskStatusChoices.SUCCESS_SCAN,
    )
    mixer.blend(
        Document,
        zone=zone,
        counter_scan_task=task,
        status=DocumentStatusChoices.READY,
    )
    employee = mixer.blend(
        Employee,
        project=project,
        roles=[EmployeeRoleChoices.COUNTER],
        serial_number=1,
        is_auto_assignment=True,
    )
    mixer.blend(
        Terminal,
        project=project,
        employee=employee,
        number=99900,
        device_model='MC2200',
    )
    return task
