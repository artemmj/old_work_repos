import csv
import logging

from rest_framework.exceptions import ValidationError

from apps import app
from apps.file.models import File
from apps.helpers.services import AbstractService
from apps.project.models import Project
from apps.template.models import Template
from apps.zone.models import Zone

logger = logging.getLogger('django')


@app.task
def import_zones_celery_wrapper(serializer_data: dict):
    """Обертка для асинхронной загрузки зон."""
    return ImportZonesService(serializer_data).process()


class ImportZonesService(AbstractService):
    """Сервис для импорта зон из файла csv или txt по шаблону."""

    def __init__(self, serializer_data: dict) -> None:
        self.zones_file: File = File.objects.get(id=serializer_data['file'])
        self.project: Project = Project.objects.get(pk=serializer_data['project'])
        self.template: Template = Template.objects.get(id=serializer_data['template'])

        if self.zones_file.file.path.split('.')[-1] not in ('csv', 'txt'):  # noqa: WPS510
            raise ValidationError('Для загрузки необходим файл формата csv или txt.')

    def process(self, *args, **kwargs):
        self._check_len_row()
        with open(self.zones_file.file.path, newline='', encoding='windows-1251') as ifile:
            reader = csv.reader(ifile, delimiter=self.template.field_separator)
            last_serial_number = self._get_last_serial_number()
            for counter, row in enumerate(reader, start=last_serial_number + 1):
                row = map(str.strip, row)
                dict_to_data = dict(zip(self.template.fields, row))
                create_data = {}

                if 'zone_name' in dict_to_data:
                    create_data['title'] = dict_to_data.get('zone_name')
                if 'zone_code' in dict_to_data:
                    create_data['code'] = dict_to_data.get('zone_code')

                create_data['serial_number'] = counter
                create_data['storage_name'] = dict_to_data.get('storage_code', 'нет')

                Zone.objects.create(project=self.project, **create_data)

        return f'Успешно обработано {reader.line_num} строк(и).'

    def _get_last_serial_number(self) -> int:
        last_serial_number = 0
        zones = Zone.objects.filter(project=self.project).order_by('serial_number')
        if zones:
            last_serial_number = zones.last().serial_number
        return last_serial_number

    def _check_len_row(self):
        with open(self.zones_file.file.path, newline='', encoding='windows-1251') as ifile:
            for row in csv.reader(ifile, delimiter=self.template.field_separator):
                if len(row) != len(self.template.fields):
                    raise ValidationError('Не совпадает количество полей в файле и полей в шаблоне!')
                break
