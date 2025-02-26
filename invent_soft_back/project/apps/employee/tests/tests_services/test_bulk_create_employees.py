import pytest

from apps.employee.models import Employee
from apps.employee.services import BulkCreateEmployeesService

pytestmark = [pytest.mark.django_db]


def test_bulk_create_employees(project):
    """Тест для проверки массового создания сотрудников."""
    employees_content = [
        {
            'id': '09ed3fe3-cfae-424c-8f05-24748d90c028',
            'serial_number': 1,
            'username': 'Сотрудник 1',
            'roles': [
                'counter',
            ],
            'is_deleted': False,
        },
        {
            'id': 'cdb58a6d-563e-48a1-b34d-9687aee3bf5d',
            'serial_number': 2,
            'username': 'Сотрудник 2',
            'roles': [
                'counter',
            ],
            'is_deleted': False,
        },
    ]

    BulkCreateEmployeesService(project, employees_content).process()

    assert Employee.objects.filter(project=project).count() == 2
