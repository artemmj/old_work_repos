import logging
from typing import List

from apps.employee.models import Employee
from apps.helpers.services import AbstractService
from apps.project.models import IssuingTaskChoices
from apps.task.models import Task, TaskTypeChoices
from apps.websocket.services import SendWebSocketInfo
from apps.zone.models import Zone

logger = logging.getLogger('django')


class IssuingTasksService(AbstractService):
    """Сервис выдачи заданий."""

    def __init__(self, zone: Zone, employees: List[Employee], role: str):
        self.zone = zone
        self.project = zone.project
        self.role = role
        self.employees = employees

        self.types_map = {
            'counter': TaskTypeChoices.COUNTER_SCAN,
            'counter_scan': TaskTypeChoices.COUNTER_SCAN,
            'controller': TaskTypeChoices.CONTROLLER,
            'auditor': TaskTypeChoices.AUDITOR,
            'auditor_controller': TaskTypeChoices.AUDITOR_CONTROLLER,
            'auditor_external': TaskTypeChoices.AUDITOR_EXTERNAL,
            'storage': TaskTypeChoices.STORAGE,
        }

    def process(self, least_loaded=False) -> list:
        """
        Выдача задания сотруднику на зону.
        :param least_loaded: True если нужно выдать задание
        с настройкой наименеезагруженному после выполнения задания С.Скан или У.Скан
        """
        new_tasks_ids = []
        for employee in self.employees:
            task_type = self.types_map.get(self.role)
            check_match_role = self._check_match_role_type(task_type)
            check_least_loaded_setts = self._check_least_loaded_setting(type, least_loaded)
            if check_match_role or check_least_loaded_setts:
                continue

            task = Task.objects.create(zone=self.zone, employee=employee, type=task_type)
            new_tasks_ids.append(task.pk)
            # Сигнал в сокет про обновление зоны
            SendWebSocketInfo().send_about_update_zones(zones=[self.zone])

        return new_tasks_ids

    def _check_match_role_type(self, type: str) -> bool:  # noqa: WPS125
        """Если нет соответствия типа задания с ролями сотрудника."""
        return self.role not in type

    def _check_least_loaded_setting(self, type: str, least_loaded: bool) -> bool:  # noqa: WPS125
        """Если настройка выдачи заданий: наименее загруженному."""
        if self.project.terminal_settings.issuing_task == IssuingTaskChoices.LEAST_LOADED_USER:
            # Если тип задания С.Скан или А.Скан и выдача задания
            # инициализированна при выполнении задания соответствующего типа
            if type in (TaskTypeChoices.COUNTER_SCAN, TaskTypeChoices.AUDITOR) and least_loaded:  # noqa: WPS510
                return True
        return False
