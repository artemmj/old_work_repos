import csv
import logging

from rest_framework.exceptions import ValidationError

from apps import app
from apps.employee.models import Employee, EmployeeRoleChoices
from apps.file.models import File
from apps.helpers.services import AbstractService
from apps.project.models import Project
from apps.template.models import Template

logger = logging.getLogger('django')


@app.task
def import_employees_celery_wrapper(serializer_data: dict):
    """Обертка для асинхронной загрузки сотрудников."""
    return ImportEmployeesService(serializer_data).process()


class ImportEmployeesService(AbstractService):
    """Сервис для импорта сотрудников из файла csv или txt по шаблону."""

    def __init__(self, serializer_data: dict) -> None:
        self.employees_file: File = File.objects.get(id=serializer_data['file'])
        self.project: Project = Project.objects.get(pk=serializer_data['project'])
        self.template: Template = Template.objects.get(id=serializer_data['template'])

        if self.employees_file.file.path.split('.')[-1] not in ('csv', 'txt'):  # noqa: WPS510
            raise ValidationError('Для загрузки необходим файл формата csv или txt.')

    def process(self, *args, **kwargs):  # noqa: WPS231
        template_fields = self.template.fields.copy()

        with open(self.employees_file.file.path, newline='', encoding='windows-1251') as f:
            reader = csv.reader(f, delimiter=self.template.field_separator)

            for idx, row in enumerate(reader):
                if idx == 0 and len(row) != len(template_fields):
                    raise ValidationError(
                        'Не совпадает количество полей в файле и полей в шаблоне. Проверьте файл и шаблон.',
                    )

                dict_to_data = dict(zip(template_fields, row))
                create_data = {}

                if 'serial_number' in dict_to_data:
                    create_data['serial_number'] = dict_to_data.get('serial_number')
                if 'full_name' in dict_to_data:
                    create_data['full_name'] = dict_to_data.get('full_name')

                try:  # noqa: WPS229
                    employee = Employee.objects.get(project=self.project, serial_number=create_data['serial_number'])
                    employee.username = create_data['full_name']
                    employee.save()
                except Employee.DoesNotExist:
                    Employee.objects.create(
                        project=self.project,
                        serial_number=create_data['serial_number'],
                        username=create_data['full_name'],
                        roles=[EmployeeRoleChoices.AUDITOR],
                    )

        return f'Успешно обработано {reader.line_num} строк(и).'
