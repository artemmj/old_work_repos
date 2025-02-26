from typing import List

from django.db.models import QuerySet

from apps.employee.models import Employee, EmployeeRoleChoices
from apps.employee.services.least_loaded import LeastLoadedEmployeeService
from apps.helpers.services import AbstractService
from apps.task.models import Task, TaskStatusChoices, TaskTypeChoices
from apps.zone.models import Zone, ZoneStatusChoices
from apps.zone.services.issuing_tasks import IssuingTasksService


class CheckAutoAssignService(AbstractService):
    """
    Сервис проверяет, что СКАН или УК выполнил все свои зоны, и, если включены настройки
    auto_zones_amount и auto_assign_enbale, выдает новую пачку зон на этого СКАН или наименее
    загруженному УК. Не выдавать на УК пользователя который назначен на СКАН в зоне.
    """

    def __init__(self, db_task: Task):
        self.db_task = db_task

    def process(self):
        project = self.db_task.zone.project
        z_amount_is_zero = project.rmm_settings.auto_zones_amount
        settings_assgn_enable = project.auto_assign_enbale
        empl_is_del = self.db_task.employee.is_deleted
        empl_is_auto_assgn = self.db_task.employee.is_auto_assignment
        if z_amount_is_zero == 0 or not settings_assgn_enable or empl_is_del or not empl_is_auto_assgn:
            return

        init_task_fields = {
            'zone__project': project,
            'employee': self.db_task.employee,
            'type': self.db_task.type,
            'status': TaskStatusChoices.INITIALIZED,
        }
        if Task.objects.filter(**init_task_fields).exists():
            return

        not_ready_zones = Zone.objects.filter(
            project=project, status=ZoneStatusChoices.NOT_READY, is_auto_assignment=True,
        ).order_by('serial_number')

        if self.db_task.type == TaskTypeChoices.COUNTER_SCAN:
            self._make_batch_tasks_counter_scan(not_ready_zones)
        elif self.db_task.type == TaskTypeChoices.CONTROLLER:
            self._make_batch_tasks_controller(not_ready_zones)

    def _make_batch_tasks_counter_scan(self, not_ready_zones: QuerySet):
        """Функция выдает auto_zones_amount заданий-на-зону СКАН для сотрудника в текущей таске."""
        counter = 0  # переменная для отсчета кол-ва выданных заданий-на-зону

        for zone in not_ready_zones:
            if not zone.tasks.filter(type=self.db_task.type):
                IssuingTasksService(zone=zone, employees=[self.db_task.employee], role=self.db_task.type).process()
                counter += 1
            if counter == self.db_task.zone.project.rmm_settings.auto_zones_amount:  # noqa: WPS219
                break

    def _check_controller_conds(self, not_ready_zone: Zone) -> bool:
        """Функция проверяет условия, при которых необходимо пропустить выдачу на зону."""
        if not_ready_zone.tasks.filter(type=TaskTypeChoices.COUNTER_SCAN, status=TaskStatusChoices.INITIALIZED):
            # Если в зоне есть активные неотработанные задания СКАН - пропустить
            return True
        elif not not_ready_zone.tasks.filter(type=TaskTypeChoices.COUNTER_SCAN):
            # или если в зоне вообще нет заданий СКАН - тоже пропустить
            return True
        elif not_ready_zone.tasks.filter(type=TaskTypeChoices.CONTROLLER):
            # Если в зоне уже есть задание УК - пропустить
            return True
        return False

    def _check_init_empl_controller_tasks(self, least_load_employee: Employee, new_added_tasks_ids: List):
        """Фукнция проверяет, что в проекте есть хотя бы 1 активное задание УК, если так - пропустить выдачу."""
        exists_empl_contrl_params = {
            'zone__project': self.db_task.zone.project,
            'employee': least_load_employee,
            'type': TaskTypeChoices.CONTROLLER,
            'status': TaskStatusChoices.INITIALIZED,
        }
        init_empl_control_tasks = Task.objects.filter(**exists_empl_contrl_params).exclude(pk__in=new_added_tasks_ids)
        return init_empl_control_tasks.exists()

    def _make_batch_tasks_controller(self, not_ready_zones: QuerySet):  # noqa: WPS231
        """Функция выдает auto_zones_amount заданий-на-зону УК для сотрудника в текущей таске + больше логики."""
        counter = 0  # переменная для отсчета кол-ва выданных заданий-на-зону
        new_added_tasks_ids = []  # массив для хранения айди выданых заданий, чтобы исключить их из фильтрации в цикле

        for not_ready_zone in not_ready_zones:
            if self._check_controller_conds(not_ready_zone):
                continue

            nzones = not_ready_zone.tasks.filter(type=TaskTypeChoices.COUNTER_SCAN).values_list('pk', flat=True)
            least_load_params = {
                'project': self.db_task.zone.project,
                'role': EmployeeRoleChoices.COUNTER,
                'task_type': self.db_task.type,
                # Если в зоне есть отработанное задание СКАН, не назначать на юзера, который делал
                'exclude_ids': list(nzones),
            }
            least_load_employee = LeastLoadedEmployeeService(**least_load_params).process()
            # Пропустить выдачу, если в проекте есть хотя бы одно активное задание УК
            # на этого пользователя. Исключить из проверки новые выданные задания
            if self._check_init_empl_controller_tasks(least_load_employee, new_added_tasks_ids):
                continue

            new_ids = IssuingTasksService(
                zone=not_ready_zone,
                employees=[least_load_employee],
                role=self.db_task.type,
            ).process()
            new_added_tasks_ids.extend(new_ids)
            counter += 1
            # Закончить, если выдали зон = настройке auto_zones_amount
            if counter == self.db_task.zone.project.rmm_settings.auto_zones_amount:  # noqa: WPS219
                break
