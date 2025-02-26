import pytest
from mixer.backend.django import mixer

from apps.document.models import DocumentStatusChoices, Document
from apps.employee.models import Employee, EmployeeRoleChoices
from apps.task.models import TaskTypeChoices, TaskStatusChoices, Task
from apps.terminal.models import Terminal
from apps.zone.models import ZoneStatusChoices, Zone

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def task_for_process_controller_work_with_recals_settings_controller_if_not_task(project):
    """
    Фикстура создания задания для проверки  функции _work_with_recals_settings_controller при условии ,
    что нет заданий УК.
    """
    zone = mixer.blend(
        Zone,
        project=project,
        serial_number=1,
        status=ZoneStatusChoices.READY,
    )
    task = mixer.blend(
        Task,
        zone=zone,
        result=187,
        type=TaskTypeChoices.CONTROLLER,
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


@pytest.fixture()
def task_for_process_controller_work_with_recals_settings_controller_if_have_task_and_equal_result(
    project,
    tasks_factory,
):
    """
    Фикстура создания задания для проверки  функции _work_with_recals_settings_controller при условии ,
    что есть задание УК и совпадают результаты.
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
        type=(type for type in [TaskTypeChoices.CONTROLLER, TaskTypeChoices.CONTROLLER, TaskTypeChoices.COUNTER_SCAN]),
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


@pytest.fixture()
def task_for_process_controller_work_with_recals_settings_controller_if_have_task_and_not_equal_result(
    project,
    tasks_factory,
):
    """
    Фикстура создания задания для проверки  функции _work_with_recals_settings_controller при условии ,
    что есть задание УК, не совпадают результаты и заданий УК в зоне меньше в 3 раза, чем СКАН.
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
        result=(result for result in [180, 187, 190, 156, 155]),
        type=(type for type in [
            TaskTypeChoices.CONTROLLER,
            TaskTypeChoices.CONTROLLER,
            TaskTypeChoices.CONTROLLER,
            TaskTypeChoices.COUNTER_SCAN,
            TaskTypeChoices.COUNTER_SCAN]
              ),
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


@pytest.fixture()
def task_for_process_controller_work_with_recals_settings_controller_if_have_controller_task_and_more_than_counter_scan(
    project,
    tasks_factory,
):
    """
    Фикстура создания задания для проверки  функции _work_with_recals_settings_controller при условии ,
    что есть задание УК, не совпадают результаты и заданий УК в зоне больше в 3 раза, чем СКАН.
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
        count=4,
        zone=zone,
        employee=employee,
        result=(result for result in [180, 187, 190, 156]),
        type=(type for type in [
            TaskTypeChoices.CONTROLLER,
            TaskTypeChoices.CONTROLLER,
            TaskTypeChoices.CONTROLLER,
            TaskTypeChoices.COUNTER_SCAN,]
              ),
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
