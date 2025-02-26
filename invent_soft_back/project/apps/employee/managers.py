from typing import OrderedDict

from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError

from apps.employee.models import Employee
from apps.event.models import Event, TitleChoices


class EmployeeManager:

    def bulk_create(self, data: OrderedDict):
        """Создание сотрудников в рамках конкретного проекта."""  # noqa: DAR401
        project = data['project']
        start_serial_number = data['start_serial_number']
        amount = data['amount']
        end_serial_number = amount + start_serial_number
        roles = data['roles']

        with transaction.atomic():
            for number in range(start_serial_number, end_serial_number):
                try:
                    Employee.objects.create(
                        project=project,
                        serial_number=number,
                        roles=roles,
                        username=f'Сотрудник {number}',
                    )
                except IntegrityError:
                    raise ValidationError(
                        f'Невозможно создать сотрудника с порядковым номером {number}, '
                        f'в рамках проекта {project.title}, так как он уже создан',  # noqa: WPS326
                    )

    def bulk_delete(self, data: OrderedDict):
        """Удаление сотрудников в рамках конкретного проекта."""
        project = data['project']
        start_serial_number = data['start_serial_number']
        end_serial_number = data['end_serial_number'] + 1

        employees = Employee.objects.filter(
            project=project, serial_number__in=range(start_serial_number, end_serial_number),
        )

        comment = f'Удалены пользователи: с {start_serial_number} по {end_serial_number - 1}:\r\n'
        for employee in employees:
            comment += f'{employee.username}\r\n'
            employee.is_deleted = True
            employee.is_auto_assignment = False
            employee.serial_number = None
            employee.save()

        Event.objects.create(project=project, title=TitleChoices.EMPLOYEES_DELETE, comment=comment)
