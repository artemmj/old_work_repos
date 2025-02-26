import logging
from typing import Dict, Generator, List, Union

from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

from apps.employee.models import Employee, EmployeeRoleChoices
from apps.helpers.services import AbstractService
from apps.project.models import Project
from apps.task.models import Task, TaskStatusChoices, TaskTypeChoices
from apps.zone.models import Zone, ZoneStatusChoices
from apps.zone.services import IssuingTasksService

logger = logging.getLogger('django')


class AutoAssignmentZoneService(AbstractService):
    """Сервис вычисления зон и сотрудников для авто выдачи заданий."""

    def __init__(self, project: Project):
        self.project = project

    def process(self, *args, **kwargs):  # noqa: WPS231
        """Выдача заданий сотрудникам на зоны."""  # noqa: DAR401
        zones = self._calculation_zones()
        employees = self._calculation_employees()

        if not zones or not employees:
            if not zones:
                raise ValidationError({'error': 'Не удалось найти зоны для автоназначения заданий'})
            if not employees:
                raise ValidationError({'error': 'Не удалось найти сотрудников для автоназначения заданий'})

        auto_zones_amount = self.project.rmm_settings.auto_zones_amount or 0
        for item in self._distribution(zones, employees, auto_zones_amount):
            for employee, zones in item.items():
                for zone in zones:
                    IssuingTasksService(zone, [employee], TaskTypeChoices.COUNTER_SCAN).process()

    def _calculation_zones(self) -> Union[QuerySet, List[Zone]]:
        """Вычисление подходящих зон для автоназначения."""
        zones = Zone.objects.filter(
            project=self.project,
            is_auto_assignment=True,
            status=ZoneStatusChoices.NOT_READY,
        ).exclude(
            tasks__type=TaskTypeChoices.COUNTER_SCAN,
        )
        return zones.order_by('serial_number')

    def _calculation_employees(self) -> Union[QuerySet, List[Employee]]:
        """Вычисление подходящих сотрудников для автоназначения."""
        employees = Employee.objects.filter(
            project=self.project,
            roles__icontains=EmployeeRoleChoices.COUNTER,
            is_auto_assignment=True,
        )
        for employee in employees:
            if Task.objects.filter(  # noqa: WPS337
                type=TaskTypeChoices.COUNTER_SCAN,
                status=TaskStatusChoices.INITIALIZED,
                employee=employee,
            ):
                employees = employees.exclude(pk=employee.pk)

        return employees.order_by('serial_number')

    def _distribution(self, zones: QuerySet, employees: QuerySet, auto_zones_amount: int) -> List[Dict]:
        """Распределение сотрудников по зонам."""
        count = 0
        result = []
        for chunk in self._chunks_of_zones(zones, auto_zones_amount):
            if chunk and count in range(0, employees.count()):
                result.append({employees[count]: chunk})
                count += 1
        return result

    def _chunks_of_zones(self, zones: Union[QuerySet, List[Zone]], n: int) -> Generator[Zone, None, None]:
        """Возвращает последовательные части разбитого списка zones по n значений в каждом."""  # noqa: DAR301
        if n > 0:
            for i in range(0, len(zones), n):  # noqa: WPS526
                yield zones[i:i + n]
