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

    def process(self, *args, **kwargs):  # noqa: WPS231
        last_serial_number = self._get_last_serial_number()
        create_zones, reader = self._prepare_create_zones(last_serial_number, self.template)
        self._bulk_create_zones(create_zones)

        return f'Успешно обработано {reader.line_num} строк(и).'

    def _get_last_serial_number(self) -> int:
        """Функция возвращает последний порядковый номер зоны."""
        last_serial_number = 0
        zones = Zone.objects.filter(project=self.project).order_by('serial_number')
        if zones:
            last_serial_number = zones.last().serial_number

        return last_serial_number

    def _prepare_create_zones(self, last_serial_number, template):  # noqa: WPS231
        """Функция для подготовки данных о зонах."""  # noqa: DAR401
        create_zones = []
        with open(self.zones_file.file.path, newline='', encoding='windows-1251') as ifile:
            reader = csv.reader(ifile, delimiter=template.field_separator)

            for counter, row in enumerate(reader, start=last_serial_number + 1):
                if counter == last_serial_number + 1 and len(row) != len(template.fields):
                    raise ValidationError(
                        'Не совпадает количество полей в файле и полей в шаблоне. Проверьте файл и шаблон.',
                    )

                zone_content = dict(zip(template.fields, row))
                create_zone = {}
                if 'zone_name' in zone_content:
                    create_zone['title'] = zone_content.get('zone_name')
                if 'storage_code' in zone_content:
                    create_zone['storage_name'] = zone_content.get('storage_code')
                if 'zone_code' in zone_content:
                    create_zone['code'] = zone_content.get('zone_code')
                create_zone['serial_number'] = counter
                create_zones.append(create_zone)

        return create_zones, reader

    def _bulk_create_zones(self, create_zones):
        """Функции для массового создания зон."""
        Zone.objects.bulk_create(
            [
                Zone(
                    project=self.project,
                    **create_zone,
                )
                for create_zone in create_zones
            ],
            ignore_conflicts=True,
        )
