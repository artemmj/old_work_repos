import pytest

from api.v1.sync.services.handle_terminal_session.check_auto_assign import CheckAutoAssignService
from apps.employee.models import Employee
from apps.project.models import Project
from apps.task.models import Task, TaskTypeChoices
from apps.terminal.models import Terminal
from apps.zone.models import Zone, ZoneStatusChoices

pytestmark = [pytest.mark.django_db]


def test_check_controller_conds(tasks_for_check_controller_conds):
    """Тест для проверки функции check_controller_conds сервиса CheckAutoAssignService"""
    project = Project.objects.first()
    project.auto_assign_enbale = True
    project.save(update_fields=['auto_assign_enbale'])
    setting_auto = project.rmm_settings
    setting_auto.auto_zones_amount = 5
    setting_auto.save(update_fields=['auto_zones_amount'])

    terminal = Terminal.objects.first()
    employee = Employee.objects.first()
    zone = Zone.objects.filter(serial_number=1).first()
    task = Task.objects.filter(type=TaskTypeChoices.COUNTER_SCAN).first()

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
            not_ready_zone = Zone.objects.filter(
                project=project, status=ZoneStatusChoices.NOT_READY, is_auto_assignment=True,
            ).order_by('serial_number').first()

            check_controller_conds = CheckAutoAssignService(task)._check_controller_conds(not_ready_zone)

            assert check_controller_conds is False
