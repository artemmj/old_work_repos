import pytest

from api.v1.sync.services.handle_terminal_session.process_counter_scan import ProcessCounterScanService
from apps.document.models import DocumentStatusChoices, DocumentColorChoices, Document
from apps.employee.models import Employee
from apps.task.models import TaskTypeChoices, Task
from apps.terminal.models import Terminal
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]


def test_make_zone_doc_ready(tasks_make_zone_doc_ready):
    """Тест для проверки функции _make_zone_doc_ready."""
    terminal = Terminal.objects.first()
    employee = Employee.objects.first()
    zone = Zone.objects.first()
    task = Task.objects.filter(type=TaskTypeChoices.COUNTER_SCAN, result=187).first()
    document_created = Document.objects.filter(color=DocumentColorChoices.VIOLET).first()
    z_controllr_task = Task.objects.filter(type=TaskTypeChoices.CONTROLLER, result=187).first()

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
            terminal = task.terminal
            ProcessCounterScanService(
                src_task,
                task,
                zone_documents,
                terminal,
            )._make_zone_doc_ready(document_created, z_controllr_task)

    assert document_created.color == DocumentColorChoices.GREEN
    assert document_created.status == DocumentStatusChoices.READY
    assert document_created.controller_task == z_controllr_task
    assert Document.objects.filter(color=DocumentColorChoices.GREEN).count() == 1
    assert Document.objects.filter(color=DocumentColorChoices.RED).count() == 3
    assert Document.objects.filter(color=DocumentColorChoices.GRAY).count() == 0
    assert Document.objects.filter(status=DocumentStatusChoices.READY).count() == 1
