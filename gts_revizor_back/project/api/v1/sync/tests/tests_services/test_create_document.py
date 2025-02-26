import pytest

from api.v1.sync.services.handle_terminal_session.create_document import CreateDocumentService
from apps.document.models import DocumentColorChoices, Document
from apps.employee.models import Employee
from apps.task.models import TaskTypeChoices, Task
from apps.terminal.models import Terminal
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]


def test_create_document(tasks_for_create_document):
    """Тест для проверки сервиса создания документа"""
    terminal = Terminal.objects.first()
    employee = Employee.objects.first()
    zone = Zone.objects.first()
    task = Task.objects.filter(type=TaskTypeChoices.COUNTER_SCAN, result=187).first()

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
            employee = task.employee
            terminal = task.terminal
            CreateDocumentService(
                src_task,
                task,
                employee,
                terminal,
            ).process()


    assert Document.objects.filter(zone__project=zone.project).count() == 3
    assert Document.objects.filter(zone__project=zone.project, color=DocumentColorChoices.VIOLET).count() == 1
    create_document = Document.objects.filter(zone__project=zone.project, color=DocumentColorChoices.VIOLET).first()
    assert create_document.counter_scan_task == task
