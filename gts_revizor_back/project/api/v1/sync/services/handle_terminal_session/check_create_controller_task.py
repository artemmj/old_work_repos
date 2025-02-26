import logging

from apps.employee.models import Employee, EmployeeRoleChoices
from apps.employee.services import LeastLoadedEmployeeService
from apps.helpers.services import AbstractService
from apps.project.models.terminal_settings_choices import IssuingTaskChoices, RecalculationDiscrepancyChoices
from apps.task.models import Task, TaskStatusChoices, TaskTypeChoices
from apps.zone.models import Zone, ZoneStatusChoices
from apps.zone.services.issuing_tasks import IssuingTasksService

logger = logging.getLogger('django')


class CheckCreateControllerTaskService(AbstractService):
    """
    Сервис для текущего переданного задания СКАН автоматически создает соотв. новое задание УК.

    В зависимости от настройки терминала проекта (terminal_settings.issuing_task) при выполнении задачи сканом
    необходимо автоматически создать новое задания для УК, при условии, что у сотрудника нет активного задания
    в зоне. Для настройки Текущий пользователь - в исполнители поставить текущего пользователя, при настройке
    Наименее загруженному пользователю - высчитать наименее загруженного и назначить на него задачу УК.
    Не создавать задания на пользователя, если на него уже есть активное задание в какой-то зоне за УК.
    """

    def __init__(self, db_zone: Zone, db_employee: Employee):
        self.db_zone = db_zone
        self.db_employee = db_employee

    def process(self) -> None:
        project = self.db_zone.project
        auto_z_amount = project.rmm_settings.auto_zones_amount == 0
        if auto_z_amount or not project.auto_assign_enbale:
            return

        recalc_sett_scan = project.terminal_settings.recalculation_discrepancy == RecalculationDiscrepancyChoices.SCAN
        zone_scan_tasks = Task.objects.filter(zone=self.db_zone, type=TaskTypeChoices.COUNTER_SCAN)
        if recalc_sett_scan and zone_scan_tasks.count() > 2:
            return

        employee = None
        if project.terminal_settings.issuing_task == IssuingTaskChoices.CURRENT_USER:
            employee = self.db_employee
        elif project.terminal_settings.issuing_task == IssuingTaskChoices.LEAST_LOADED_USER:
            employee = LeastLoadedEmployeeService(
                project=project,
                role=EmployeeRoleChoices.COUNTER,
                task_type=TaskTypeChoices.CONTROLLER,
                exclude_ids=[self.db_employee.pk],
            ).process()

        if not employee:
            return

        controller_employee_init_tasks = Task.objects.filter(
            employee=employee, type=TaskTypeChoices.CONTROLLER, status=TaskStatusChoices.INITIALIZED,
        )
        if controller_employee_init_tasks.count() < project.rmm_settings.auto_zones_amount:
            IssuingTasksService(zone=self.db_zone, employees=[employee], role=TaskTypeChoices.CONTROLLER).process()
