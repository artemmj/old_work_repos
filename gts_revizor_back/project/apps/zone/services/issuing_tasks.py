import logging
from typing import List

from apps.employee.models import Employee
from apps.helpers.services import AbstractService
from apps.task.models import Task, TaskTypeChoices
from apps.websocket.services import SendWebSocketService
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
        self.new_tasks_ids = []

    def process(self) -> List[str]:
        """Выдача задания сотрудникам на зону."""
        for employee in self.employees:
            task = Task.objects.create(zone=self.zone, employee=employee, type=self.types_map.get(self.role))
            self.new_tasks_ids.append(task.pk)
            # Сигнал в сокет про обновление зоны
            SendWebSocketService().send_about_update_zones(zones=[self.zone])
        return self.new_tasks_ids
