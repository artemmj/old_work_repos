import pytest

from apps.employee.models import EmployeeRoleChoices
from apps.employee.services.get_employees import GetEmployeesService
from apps.task.models import TaskTypeChoices, TaskStatusChoices

pytestmark = [pytest.mark.django_db]


def test_get_employees_successful(project, employee_factory, tasks_factory):
    """Тест для проверки получения сотрудников."""
    employees = employee_factory(
        count=5,
        project=project,
        roles=(role for role in [
            [EmployeeRoleChoices.COUNTER],
            [EmployeeRoleChoices.COUNTER],
            [EmployeeRoleChoices.COUNTER],
            [EmployeeRoleChoices.AUDITOR],
            [EmployeeRoleChoices.COUNTER],
        ]),
        is_deleted=(is_deleted for is_deleted in [False, True, False, False, False]),
    )

    for employee in employees:
        tasks_factory(
            count=5,
            employee=employee,
            type=TaskTypeChoices.COUNTER_SCAN,
            status=(status for status in (
                TaskStatusChoices.INITIALIZED,
                TaskStatusChoices.SUCCESS_SCAN,
                TaskStatusChoices.INITIALIZED,
                TaskStatusChoices.INITIALIZED,
                TaskStatusChoices.FAILED_SCAN,
            )),
        )

    created_employees = GetEmployeesService().process()

    created_employee = created_employees.first()

    assert created_employees.count() == 4
    assert len(created_employee.initialized_tasks) == 3
