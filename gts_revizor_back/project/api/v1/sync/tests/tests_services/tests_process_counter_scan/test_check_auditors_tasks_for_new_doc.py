import pytest

from api.v1.sync.services.handle_terminal_session.process_counter_scan import ProcessCounterScanService
from apps.document.models import DocumentColorChoices, Document
from apps.employee.models import Employee
from apps.task.models import TaskTypeChoices, Task, TaskStatusChoices
from apps.terminal.models import Terminal
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]


def test_check_auditors_tasks_for_new_doc(task_for_check_auditors_tasks_for_new_doc):
    """Тест для проверки функции _check_auditors_tasks_for_new_doc"""
    terminal = Terminal.objects.first()
    employee = Employee.objects.first()
    zone = Zone.objects.first()
    task = Task.objects.filter(type=TaskTypeChoices.COUNTER_SCAN, result=187).first()
    new_doc = Document.objects.filter(color=DocumentColorChoices.VIOLET).first()
    auditor_zone_tasks = Task.objects.filter(zone=zone, type=TaskTypeChoices.AUDITOR)
    auditor_zone_tasks = auditor_zone_tasks.exclude(status=TaskStatusChoices.INITIALIZED).order_by('created_at')
    auditor_ext_zone_tasks = Task.objects.filter(zone=zone, type=TaskTypeChoices.AUDITOR_EXTERNAL)
    auditor_ext_zone_tasks = auditor_ext_zone_tasks.exclude(
        status=TaskStatusChoices.INITIALIZED,
    ).order_by(
        'created_at',
    )
    auditor_contr_zone_tasks = Task.objects.filter(zone=zone, type=TaskTypeChoices.AUDITOR_CONTROLLER)
    auditor_contr_zone_tasks = auditor_contr_zone_tasks.exclude(status=TaskStatusChoices.INITIALIZED)

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
            zone = task.zone
            terminal = task.terminal
            ProcessCounterScanService(
                src_task,
                task,
                employee,
                terminal,
            )._check_auditors_tasks_for_new_doc(new_doc)

    assert new_doc.auditor_task == auditor_zone_tasks.last()
    assert new_doc.auditor_external_task == auditor_ext_zone_tasks.last()
    assert new_doc.auditor_controller_task == auditor_contr_zone_tasks.last()
