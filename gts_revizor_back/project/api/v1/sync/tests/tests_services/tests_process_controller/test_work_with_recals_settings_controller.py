import pytest

from api.v1.sync.services.handle_terminal_session.process_controller import ProcessControllerService
from apps.document.models import Document
from apps.employee.models import Employee
from apps.task.models import TaskTypeChoices, TaskStatusChoices, Task
from apps.terminal.models import Terminal
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]


def test_for_process_controller_work_with_recals_settings_controller_if_not_task(
    task_for_process_controller_work_with_recals_settings_controller_if_not_task,
):
    """Тест для проверки кол-ва тасок при условии когда отсутствуют задания УК."""
    zone = process_work_with_recals_settings_controller()

    assert Task.objects.filter(zone__project=zone.project, type=TaskTypeChoices.CONTROLLER).count() == 2
    assert Task.objects.filter(zone__project=zone.project, type=TaskTypeChoices.COUNTER_SCAN).count() == 0


def test_or_process_controller_work_with_recals_settings_controller_if_have_task_and_equal_result(
    task_for_process_controller_work_with_recals_settings_controller_if_have_task_and_equal_result,
):
    """Тест для проверки кол-ва тасок при условии, что задание УК = 1 и совпадают результаты."""
    zone = process_work_with_recals_settings_controller()

    assert Task.objects.filter(zone__project=zone.project, type=TaskTypeChoices.CONTROLLER).count() == 2
    assert Task.objects.filter(zone__project=zone.project, type=TaskTypeChoices.COUNTER_SCAN).count() == 2


def test_or_process_controller_work_with_recals_settings_controller_if_have_task_and_not_equal_result(
    task_for_process_controller_work_with_recals_settings_controller_if_have_task_and_not_equal_result,
):
    """
    Тест для проверки кол-ва тасок при условии, что есть задание УК,
     не совпадают результаты и заданий УК в зоне меньше в 3 раза, чем СКАН.
     """
    zone = process_work_with_recals_settings_controller()

    assert Task.objects.filter(zone__project=zone.project, type=TaskTypeChoices.CONTROLLER).count() == 4
    assert Task.objects.filter(zone__project=zone.project, type=TaskTypeChoices.COUNTER_SCAN).count() == 2


def test_or_process_controller_work_with_recals_settings_controller_if_have_controller_task_and_more_than_counter_scan(
    task_for_process_controller_work_with_recals_settings_controller_if_have_controller_task_and_more_than_counter_scan,
):
    """
    Тест для проверки кол-ва тасок при условии, что есть задание УК,
     не совпадают результаты и заданий УК в зоне больше в 3 раза, чем СКАН.
     """
    zone = process_work_with_recals_settings_controller()

    assert Task.objects.filter(zone__project=zone.project, type=TaskTypeChoices.CONTROLLER).count() == 3
    assert Task.objects.filter(zone__project=zone.project, type=TaskTypeChoices.COUNTER_SCAN).count() == 2


def process_work_with_recals_settings_controller():
    terminal = Terminal.objects.first()
    employee = Employee.objects.first()
    zone = Zone.objects.first()
    task = Task.objects.filter(type=TaskTypeChoices.CONTROLLER).first()
    worked_statuses = (TaskStatusChoices.WORKED, TaskStatusChoices.SUCCESS_SCAN, TaskStatusChoices.FAILED_SCAN)
    zone_counter_scan_tasks = Task.objects.filter(
        zone=zone, type=TaskTypeChoices.COUNTER_SCAN, status__in=worked_statuses,
    )
    zone_counter_scan_tasks.update(status=TaskStatusChoices.FAILED_SCAN)

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
            )._work_with_recals_settings_controller(
                zone_counter_scan_tasks,
            )
    return zone
