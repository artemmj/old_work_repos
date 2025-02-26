import pytest

from api.v1.sync.services.handle_terminal_session.check_create_controller_task import CheckCreateControllerTaskService
from apps.document.models import DocumentStatusChoices, Document
from apps.employee.models import Employee, EmployeeRoleChoices
from apps.project.models import Project, IssuingTaskChoices
from apps.task.models import TaskTypeChoices, TaskStatusChoices, Task
from apps.terminal.models import Terminal
from apps.zone.models import ZoneStatusChoices, Zone

pytestmark = [pytest.mark.django_db]


def test_check_create_controller_task_current_user(tasks_for_check_create_controller_task):
    """
    Тест для проверки сервиса CheckCreateControllerTaskService
    с настройкой Выдача задания для УК текущему пользователю.
    """
    project = Project.objects.first()
    project.auto_assign_enbale = True
    project.save(update_fields=['auto_assign_enbale'])
    setting_auto = project.rmm_settings
    setting_auto.auto_zones_amount = 5
    setting_auto.save(update_fields=['auto_zones_amount'])
    project.terminal_settings.issuing_task = IssuingTaskChoices.CURRENT_USER
    project.terminal_settings.save(update_fields=['issuing_task'])
    employee = Employee.objects.filter(serial_number=1).first()

    process_check_create_controller_task()

    assert Task.objects.filter(type=TaskTypeChoices.CONTROLLER).count() == 3
    assert Task.objects.filter(
        employee=employee,
        type=TaskTypeChoices.CONTROLLER,
        status=TaskStatusChoices.INITIALIZED,
    ).count() == 1


def testcheck_create_controller_task_least_loaded_user(tasks_for_check_create_controller_task):
    """
    Тест для проверки сервиса CheckCreateControllerTaskService
    с настройкой Выдача задания для УК наименее загруженному пользователю.
    """
    project = Project.objects.first()
    project.auto_assign_enbale = True
    project.save(update_fields=['auto_assign_enbale'])
    setting_auto = project.rmm_settings
    setting_auto.auto_zones_amount = 5
    setting_auto.save(update_fields=['auto_zones_amount'])
    employee = Employee.objects.filter(serial_number=1).first()
    employee_less_loaded = Employee.objects.filter(serial_number=2).first()

    process_check_create_controller_task()

    assert Task.objects.filter(type=TaskTypeChoices.CONTROLLER).count() == 3
    assert Task.objects.filter(
        employee=employee_less_loaded,
        type=TaskTypeChoices.CONTROLLER,
        status=TaskStatusChoices.INITIALIZED,
    ).count() == 1
    assert Task.objects.filter(
        employee=employee,
        type=TaskTypeChoices.CONTROLLER,
        status=TaskStatusChoices.INITIALIZED,
    ).count() == 0


def process_check_create_controller_task():
    terminal = Terminal.objects.first()
    employee = Employee.objects.first()
    zone = Zone.objects.first()
    task = Task.objects.first()

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
            zone = Zone.objects.get(pk=src_task['document']['zone'])
            employee = task.employee

            CheckCreateControllerTaskService(zone, employee).process()
