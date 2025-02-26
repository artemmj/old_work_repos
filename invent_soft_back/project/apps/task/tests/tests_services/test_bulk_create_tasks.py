import pytest

from apps.employee.models import Employee
from apps.task.models import Task
from apps.task.services import BulkCreateTasksService
from apps.terminal.models import Terminal
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]


def test_bulk_create_tasks(project_for_bulk_create_tasks):
    """Тест для проверки массового создания заданий."""
    terminal_id = Terminal.objects.filter(project=project_for_bulk_create_tasks).first().id
    zone_id = Zone.objects.filter(project=project_for_bulk_create_tasks).first().id
    employee_id = Employee.objects.filter(project=project_for_bulk_create_tasks).first().id
    tasks_content = [
        {
            'id': '7695577f-601b-41bd-b277-a92462c50b1c',
            'terminal_id': terminal_id,
            'zone_id': zone_id,
            'type': 'counter_scan',
            'status': 'worked',
            'result': '105.000',
            'employee_id': employee_id,
        },
        {
            'id': '07777bf4-78fd-4778-a805-d8f4b5f5deb0',
            'terminal_id': terminal_id,
            'zone_id': zone_id,
            'type': 'counter_scan',
            'status': 'worked',
            'result': '10.000',
            'employee_id': employee_id,
        },
    ]

    BulkCreateTasksService(tasks_content).process()

    assert Task.objects.filter(zone__project=project_for_bulk_create_tasks).count() == 2
