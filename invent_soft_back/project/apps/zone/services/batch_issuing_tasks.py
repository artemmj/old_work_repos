import logging
from typing import Iterable

from apps.employee.models import Employee
from apps.helpers.services import AbstractService
from apps.project.models import IssuingTaskChoices, Project
from apps.task.models import Task, TaskTypeChoices
from apps.zone.models import Zone

logger = logging.getLogger('django')


class BatchIssuingTasksService(AbstractService):
    """Сервис выдачи заданий."""

    def __init__(self, zones: Iterable[Zone], employees: Iterable[Employee], role: str, project):
        self.zones = zones
        self.project = project
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
        task_type = self.types_map.get(self.role)

        if self._check_least_loaded_setting(task_type, least_loaded):
            return None

        tasks_content = [
            {
                'zone': zone,
                'employee': employee,
                'task_type': task_type,
            }
            for zone in self._get_zones()
            for employee in self._get_employees()
            if not self._check_match_role_type(task_type)
        ]

        return Task.objects.bulk_create(
            [
                Task(
                    zone=task_content.get('zone'),
                    employee=task_content.get('employee'),
                    type=task_content.get('task_type'),
                )
                for task_content in tasks_content
            ],
            ignore_conflicts=True,
            batch_size=5000,
        )

    def _get_zones(self):
        yield from (
            zone
            for zone in self.zones
        )

    def _get_employees(self):
        yield from (
            employee
            for employee in self.employees
        )

    def _check_match_role_type(self, task_type: str) -> bool:
        """Если нет соответствия типа задания с ролями сотрудника."""
        return self.role not in task_type

    def _check_least_loaded_setting(self, task_type: str, least_loaded: bool) -> bool:
        """Если настройка выдачи заданий: наименее загруженному."""
        if self.project.terminal_settings.issuing_task == IssuingTaskChoices.LEAST_LOADED_USER:
            if task_type in {TaskTypeChoices.COUNTER_SCAN, TaskTypeChoices.AUDITOR} and least_loaded:
                return True
        return False
