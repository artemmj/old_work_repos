import pytest

from api.v1.sync.services.handle_terminal_session.process_counter_scan import ProcessCounterScanService
from apps.document.models import Document
from apps.employee.models import Employee
from apps.project.models import Project, RecalculationDiscrepancyChoices
from apps.task.models import TaskTypeChoices, Task
from apps.terminal.models import Terminal
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]


def test_for_assign_tasks_if_fail_if_recal_discrepancy_is_scan_and_auto_zones_amount_less_0(
    task_for_assign_tasks_if_fail_if_recal_discrepancy_is_scan_and_auto_zones_amount_less_0,
):
    """
    Тест для проверки функции _assign_tasks_if_fail
    при условии RecalculationDiscrepancyChoices.SCAN и auto_zones_amount < 0.
    """
    project = process_assign_tasks_if_fail()

    assert Task.objects.filter(zone__project=project, type=TaskTypeChoices.COUNTER_SCAN).count() == 2


def test_for_assign_tasks_if_fail_if_recal_discrepancy_is_scan_and_auto_zones_amount_more_0_zone_cs_tasks_less_3(
    task_for_assign_tasks_if_fail_if_recal_discrepancy_is_scan_and_auto_zones_amount_more_0_zone_cs_tasks_less_3,
):
    """
    Тест для проверки функции _assign_tasks_if_fail
    при условии RecalculationDiscrepancyChoices.SCAN и auto_zones_amount > 0 и заданий COUNTER_SCAN < 3.
    """
    project = Project.objects.first()
    setting_auto = project.rmm_settings
    setting_auto.auto_zones_amount = 5
    setting_auto.save(update_fields=['auto_zones_amount'])
    project = process_assign_tasks_if_fail()

    assert Task.objects.filter(zone__project=project, type=TaskTypeChoices.COUNTER_SCAN).count() == 3


def test_for_assign_tasks_if_fail_if_recal_discrepancy_is_scan_and_auto_zones_amount_more_0_zone_cs_tasks_more_3(
    task_for_assign_tasks_if_fail_if_recal_discrepancy_is_scan_and_auto_zones_amount_more_0_zone_cs_tasks_more_3
):
    """
    Тест для проверки функции _assign_tasks_if_fail
    при условии RecalculationDiscrepancyChoices.SCAN и auto_zones_amount > 0 и заданий COUNTER_SCAN > 3.
    """
    project = Project.objects.first()
    setting_auto = project.rmm_settings
    setting_auto.auto_zones_amount = 5
    setting_auto.save(update_fields=['auto_zones_amount'])
    project = process_assign_tasks_if_fail()

    assert Task.objects.filter(zone__project=project, type=TaskTypeChoices.COUNTER_SCAN).count() == 4


def test_for_assign_tasks_if_fail_if_recal_discrepancy_controller(
    task_for_assign_tasks_if_fail_if_recal_discrepancy_controller,
):
    """
    Тест для проверки функции _assign_tasks_if_fail
    при условии RecalculationDiscrepancyChoices.CONTROLLER .
    """
    project = Project.objects.first()
    setting_recalc = project.terminal_settings
    setting_recalc.recalculation_discrepancy = RecalculationDiscrepancyChoices.CONTROLLER
    setting_recalc.save(update_fields=['recalculation_discrepancy'])
    project = process_assign_tasks_if_fail()

    assert Task.objects.filter(zone__project=project, type=TaskTypeChoices.CONTROLLER).count() == 2


def process_assign_tasks_if_fail():
    terminal = Terminal.objects.first()
    employee = Employee.objects.first()
    zone = Zone.objects.first()
    task = Task.objects.filter(type=TaskTypeChoices.COUNTER_SCAN, result=187).first()
    project = task.zone.project

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
            )._assign_tasks_if_fail(project, employee)

    return project
