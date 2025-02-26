import pytest
from mixer.backend.django import mixer

from apps.document.models import DocumentStatusChoices, DocumentColorChoices
from apps.employee.models import Employee, EmployeeRoleChoices
from apps.task.models import TaskTypeChoices, TaskStatusChoices
from apps.terminal.models import Terminal
from apps.zone.models import ZoneStatusChoices, Zone

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def task_for_assign_tasks_if_fail_if_recal_discrepancy_is_scan_and_auto_zones_amount_less_0(
    project,
    tasks_factory,
    documents_factory,
):
    """
    Фикстура создания тасок для проверки функции _assign_tasks_if_fail
    при условии RecalculationDiscrepancyChoices.SCAN и auto_zones_amount < 0.
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
        count=3,
        zone=zone,
        counter_scan_task=tasks[-1],
        status=(status for status in [
            DocumentStatusChoices.READY,
            DocumentStatusChoices.READY,
            DocumentStatusChoices.NOT_READY,
        ]),
        color=(color for color in [
            DocumentColorChoices.GREEN,
            DocumentColorChoices.GREEN,
            DocumentColorChoices.VIOLET,
        ]),
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
def task_for_assign_tasks_if_fail_if_recal_discrepancy_is_scan_and_auto_zones_amount_more_0_zone_cs_tasks_less_3(
    project,
    tasks_factory,
    documents_factory,
):
    """
    Фикстура создания тасок для проверки функции _assign_tasks_if_fail
    при условии RecalculationDiscrepancyChoices.SCAN и auto_zones_amount > 0 и заданий COUNTER_SCAN < 3.
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
        count=3,
        zone=zone,
        employee=employee,
        result=187,
        type=(type for type in
              [TaskTypeChoices.CONTROLLER, TaskTypeChoices.COUNTER_SCAN, TaskTypeChoices.COUNTER_SCAN, ]),
        status=(status for status in [
            TaskStatusChoices.SUCCESS_SCAN,
            TaskStatusChoices.INITIALIZED,
            TaskStatusChoices.SUCCESS_SCAN,
        ]
                ),
    )
    documents_factory(
        count=3,
        zone=zone,
        serial_number=(serial_number for serial_number in [1, 2, 3]),
        counter_scan_task=tasks[-1],
        status=(status for status in [
            DocumentStatusChoices.READY,
            DocumentStatusChoices.READY,
            DocumentStatusChoices.NOT_READY,
        ]),
        color=(color for color in [
            DocumentColorChoices.GREEN,
            DocumentColorChoices.GREEN,
            DocumentColorChoices.VIOLET,
        ]),
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
def task_for_assign_tasks_if_fail_if_recal_discrepancy_is_scan_and_auto_zones_amount_more_0_zone_cs_tasks_more_3(
    project,
    tasks_factory,
    documents_factory,
):
    """
    Фикстура создания тасок для проверки функции _assign_tasks_if_fail
    при условии RecalculationDiscrepancyChoices.SCAN и auto_zones_amount > 0 и заданий COUNTER_SCAN > 3.
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
        count=5,
        zone=zone,
        employee=employee,
        result=187,
        type=(type for type in [
            TaskTypeChoices.CONTROLLER,
            TaskTypeChoices.COUNTER_SCAN,
            TaskTypeChoices.COUNTER_SCAN,
            TaskTypeChoices.COUNTER_SCAN,
            TaskTypeChoices.COUNTER_SCAN,
        ]
              ),
        status=(status for status in [
            TaskStatusChoices.SUCCESS_SCAN,
            TaskStatusChoices.INITIALIZED,
            TaskStatusChoices.SUCCESS_SCAN,
            TaskStatusChoices.SUCCESS_SCAN,
            TaskStatusChoices.SUCCESS_SCAN,
        ]
                ),
    )
    documents_factory(
        count=3,
        zone=zone,
        serial_number=(serial_number for serial_number in [1, 2, 3]),
        counter_scan_task=tasks[-1],
        status=(status for status in [
            DocumentStatusChoices.READY,
            DocumentStatusChoices.READY,
            DocumentStatusChoices.NOT_READY,
        ]),
        color=(color for color in [
            DocumentColorChoices.GREEN,
            DocumentColorChoices.GREEN,
            DocumentColorChoices.VIOLET,
        ]),
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
def task_for_assign_tasks_if_fail_if_recal_discrepancy_controller(
    project,
    tasks_factory,
    documents_factory,
):
    """
    Фикстура создания тасок для проверки функции _assign_tasks_if_fail
    при условии RecalculationDiscrepancyChoices.CONTROLLER.
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
        count=3,
        zone=zone,
        serial_number=(serial_number for serial_number in [1, 2, 3]),
        counter_scan_task=tasks[-1],
        status=(status for status in [
            DocumentStatusChoices.READY,
            DocumentStatusChoices.READY,
            DocumentStatusChoices.NOT_READY,
        ]),
        color=(color for color in [
            DocumentColorChoices.GREEN,
            DocumentColorChoices.GREEN,
            DocumentColorChoices.VIOLET,
        ]),
    )
    mixer.blend(
        Terminal,
        project=project,
        employee=employee,
        number=99900,
        device_model='MC2200',
    )
    return tasks
