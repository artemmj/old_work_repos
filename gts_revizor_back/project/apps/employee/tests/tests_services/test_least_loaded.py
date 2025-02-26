import pytest

from apps.employee.models import EmployeeRoleChoices
from apps.employee.services import LeastLoadedEmployeeService
from apps.task.models import TaskTypeChoices, TaskStatusChoices

pytestmark = [pytest.mark.django_db]


def test_least_loaded(project, employee_factory, tasks_factory):
    """Тест для проверки наименее загруженного сотрудника"""
    employees = employee_factory(
        count=7,
        project=project,
        serial_number=(number for number in [1, 7, 3, 0, 2, 5, 4]),
        roles=(role for role in [
                [EmployeeRoleChoices.COUNTER],
                [EmployeeRoleChoices.COUNTER],
                [EmployeeRoleChoices.COUNTER],
                [EmployeeRoleChoices.AUDITOR],
                [EmployeeRoleChoices.COUNTER],
                [EmployeeRoleChoices.COUNTER],
                [EmployeeRoleChoices.COUNTER],
        ]),
        is_deleted=(is_deleted for is_deleted in [False, True, False, False, False, False, False]),
        is_auto_assignment=(is_auto_assignment for is_auto_assignment in [True, False, False, True, True, True, True]),
    )
    for employee in employees[:5]:
        tasks_factory(
            count=5,
            employee=employee,
            type=TaskTypeChoices.COUNTER_SCAN,
            status=TaskStatusChoices.INITIALIZED,
        )
    for employee in employees[5:]:
        tasks_factory(
            count=2,
            employee=employee,
            type=TaskTypeChoices.COUNTER_SCAN,
            status=TaskStatusChoices.INITIALIZED,
        )

    least_loaded_employee = LeastLoadedEmployeeService(
        project,
        EmployeeRoleChoices.COUNTER,
        [employees[0].id],
        TaskTypeChoices.COUNTER_SCAN,
    ).process()

    assert least_loaded_employee.serial_number == 4
    assert least_loaded_employee == employees[6]
