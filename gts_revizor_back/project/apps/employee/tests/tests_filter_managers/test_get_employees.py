import pytest

from apps.employee.filter_managers import EmployeeFilterManager
from apps.employee.models import EmployeeRoleChoices, Employee
from apps.task.models import TaskTypeChoices, TaskStatusChoices

pytestmark = [pytest.mark.django_db]


def test_get_employees(project, employee_factory, tasks_factory):
    """Тест для проверки получения сотрудников c заданиями в статусе инициализированы для работы."""
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
    employees = Employee.objects.all()

    filter_employees = EmployeeFilterManager().get_employee(employees)

    filter_employee = filter_employees.first()

    assert filter_employees.count() == 4
    assert len(filter_employee.initialized_tasks) == 3
