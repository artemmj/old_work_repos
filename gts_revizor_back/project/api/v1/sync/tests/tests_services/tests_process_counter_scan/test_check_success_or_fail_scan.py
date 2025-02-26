import pytest

from api.v1.sync.services.handle_terminal_session.process_counter_scan import ProcessCounterScanService
from apps.document.models import DocumentColorChoices, Document
from apps.employee.models import Employee
from apps.task.models import TaskTypeChoices, Task, TaskStatusChoices
from apps.terminal.models import Terminal
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]


def test_check_success_or_fail_scan_in_case_task_controller_with_status_success_scan(
    tasks_check_success_or_fail_scan_in_case_task_controller_with_status_success_scan
):
    """
    Тест для проверки функции _check_success_or_fail_scan
    при наличии TaskTypeChoices.CONTROLLER со статусом SUCCESS_SCAN.
    """
    zone = Zone.objects.first()
    z_controller_worked_tasks = Task.objects.filter(
        zone=zone,
        type=TaskTypeChoices.CONTROLLER,
    ).exclude(
        status=TaskStatusChoices.INITIALIZED,
    ).order_by('created_at')

    match, success_controller_task = process_check_success_or_fail_scan()

    assert match is True
    assert success_controller_task == z_controller_worked_tasks.last()


def test_check_success_or_fail_scan_in_case_task_controller_with_status_initialized(
    tasks_check_success_or_fail_scan_in_case_task_controller_with_status_initialized
):
    """
    Тест для проверки функции _check_success_or_fail_scan
    при наличии TaskTypeChoices.CONTROLLER со статусом INITIALIZED.
    """
    match, success_controller_task = process_check_success_or_fail_scan()

    assert match is False
    assert success_controller_task is None


def process_check_success_or_fail_scan():
    terminal = Terminal.objects.first()
    employee = Employee.objects.first()
    zone = Zone.objects.first()
    task = Task.objects.filter(type=TaskTypeChoices.COUNTER_SCAN, result=187).first()
    document_created = Document.objects.filter(color=DocumentColorChoices.VIOLET).first()
    z_controller_worked_tasks = Task.objects.filter(
        zone=zone,
        type=TaskTypeChoices.CONTROLLER,
    ).exclude(
        status=TaskStatusChoices.INITIALIZED,
    ).order_by('created_at')

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
            match, success_controller_task = ProcessCounterScanService(
                src_task,
                task,
                zone_documents,
                terminal,
            )._check_success_or_fail_scan(z_controller_worked_tasks, document_created)
            return match, success_controller_task
