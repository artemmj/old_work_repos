import pytest

from api.v1.sync.services.handle_terminal_session.process_controller import ProcessControllerService
from apps.document.models import DocumentStatusChoices, Document
from apps.employee.models import Employee
from apps.task.models import TaskTypeChoices, Task, TaskStatusChoices
from apps.terminal.models import Terminal
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]


def test_check_documents_match_if_equal_result(tasks_for_check_documents_match_if_equal_result):
    """
    Тест проверки функции _check_documents_match_ при условии,
    что равны результаты counter_scan_task и db_task.
    """
    match, zone = process_match()

    assert match is True
    assert Task.objects.filter(
        zone__project=zone.project,
        type=TaskTypeChoices.COUNTER_SCAN,
        status=TaskStatusChoices.INITIALIZED,
    ).count() == 0
    assert Document.objects.filter(zone__project=zone.project, status=DocumentStatusChoices.READY).count() == 1


def test_check_documents_match_if_not_equal_result(tasks_for_check_documents_match_if_not_equal_result):
    """
    Тест проверки функции _check_documents_match_при условии,
    что результаты counter_scan_task и db_task не равны.
    """
    match, zone = process_match()
    db_task = Task.objects.filter(zone__project=zone.project, type=TaskTypeChoices.CONTROLLER, result=187).first()

    assert match is False
    assert db_task.status == TaskStatusChoices.FAILED_SCAN


def process_match():
    terminal = Terminal.objects.first()
    employee = Employee.objects.first()
    zone = Zone.objects.first()
    task = Task.objects.filter(type=TaskTypeChoices.CONTROLLER, result=187).first()

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
            match = ProcessControllerService(
                src_task,
                task,
                zone_documents,
            )._check_documents_match()
            return match, zone
