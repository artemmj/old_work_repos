import pytest

from api.v1.sync.services.handle_terminal_session.process_controller import ProcessControllerService
from apps.document.models import Document
from apps.employee.models import Employee
from apps.task.models import TaskTypeChoices, TaskStatusChoices, Task
from apps.terminal.models import Terminal
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]


def test_assign_if_fail(tasks_for_assign_if_fail):
    """Тест для проверки кол-ва и статус заданий функции _assign_if_fail."""
    terminal = Terminal.objects.first()
    employee = Employee.objects.first()
    zone = Zone.objects.first()
    task = Task.objects.filter(type=TaskTypeChoices.CONTROLLER).first()

    serializer_data = {
        'terminal_time': '2024-05-06T08:59:03.448Z',
        'terminal': terminal.id,
        'users': [
            {
                'id': employee.id,
                'tasks': [
                    {
                        'document': {
                            'employee': employee.id,
                            'end_audit_date': '2024-05-06T08:59:03.448Z',
                            'tsd_number': terminal.number,
                            'zone': zone.id,
                        },
                        'result': 187,
                        'id': task.id,
                        'scanned_products': [
                            {
                                'added_by_product_code': False,
                                'amount': 99,
                                'product': '4620123023081',
                                'is_weight_product': False,
                            },
                            {
                                'added_by_product_code': False,
                                'amount': 77,
                                'product': '4620123088134',
                                'is_weight_product': False,
                            },
                            {
                                'added_by_product_code': False,
                                'amount': 11,
                                'product': '4620123020974',
                                'is_weight_product': False,
                            }
                        ]
                    }
                ]
            }
        ]
    }
    for srcuser in serializer_data.get('users'):
        for src_task in srcuser.get('tasks'):
            task = Task.objects.get(pk=src_task['id'])
            zone = Zone.objects.get(pk=src_task['document']['zone'])
            zone_documents = Document.objects.filter(zone=zone).order_by('created_at')
            ProcessControllerService(
                src_task,
                task,
                zone_documents,
            )._assign_if_fail()

        assert task.status == TaskStatusChoices.FAILED_SCAN

    assert Task.objects.filter(zone__project=zone.project, type=TaskTypeChoices.CONTROLLER).count() == 2
    assert Task.objects.filter(zone__project=zone.project, type=TaskTypeChoices.COUNTER_SCAN).count() == 2
