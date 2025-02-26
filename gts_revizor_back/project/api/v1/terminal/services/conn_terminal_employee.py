from datetime import datetime
from typing import Dict

from rest_framework.exceptions import ValidationError

from apps.employee.models import Employee
from apps.helpers.services import AbstractService
from apps.terminal.models import Terminal


class ConnTerminalEmployeeService(AbstractService):
    """Сервис закрепляет пользователя за переданным терминалом."""

    def process(self, serializer_data: Dict):
        empl_number: int = serializer_data.get('employee_number')
        terminal = Terminal.objects.get(pk=serializer_data.get('terminal'))

        try:
            empl = Employee.objects.get(serial_number=empl_number, project=terminal.project)
        except Employee.DoesNotExist:
            raise ValidationError({'employee': f'Не найден сотрудник, номер {empl_number} проект {terminal.project}.'})

        Terminal.objects.filter(employee=empl, project=terminal.project).update(employee=None)
        terminal.employee = empl
        terminal.db_loading = True  # TODO
        terminal.last_connect = datetime.now()
        terminal.save()
        return terminal
