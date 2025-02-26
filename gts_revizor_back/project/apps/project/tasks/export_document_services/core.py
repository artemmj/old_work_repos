import logging
import os
from secrets import token_urlsafe
from typing import Dict

from django.utils import timezone

from apps import app
from apps.event.models import Event, TitleChoices
from apps.file.models import File
from apps.helpers.services import AbstractService
from apps.project.models.project import Project
from apps.project.tasks.export_document_services.write_doc_discrepancy_field import WriteDocDiscrepancyFieldService
from apps.project.tasks.export_document_services.write_doc_zone_first import WriteDocZoneFirstService
from apps.project.tasks.export_document_services.write_single_doc import WriteSingleDocService
from apps.project.tasks.export_document_services.write_standard_doc import WriteStandardDocService
from apps.template.models.template import Template, TemplateExport
from apps.template.models.template_choices import TemplateExportFieldChoices

logger = logging.getLogger('django')


@app.task
def export_document_celery_wrapper(serializer_data: Dict):
    """Асинхронная обертка для сервиса."""
    return ExportDocumentService(
        project_id=serializer_data.get('project'),
        template_id=serializer_data.get('template'),
        file_format=serializer_data.get('format'),
    ).process()


class ExportDocumentService(AbstractService):
    def __init__(self, project_id: str, template_id: str, file_format: str):
        self.project = Project.objects.get(pk=project_id)
        self.template = TemplateExport.objects.get(pk=template_id)
        self.file_format = file_format

    def process(self, *args, **kwargs):
        filepath, file = self._create_db_file()
        is_discrepancy_field = TemplateExportFieldChoices.DISCREPANCY in self.template.fields
        is_discrepancy_decimal_field = TemplateExportFieldChoices.DISCREPANCY_DECIMAL in self.template.fields
        is_zone_name_field = TemplateExportFieldChoices.ZONE_NAME in self.template.fields
        is_zone_number_field = TemplateExportFieldChoices.ZONE_NUMBER in self.template.fields

        zone_number_start, zone_number_end = self._get_first_and_last_zone_numbers()

        if self.template.single_export:
            WriteSingleDocService(
                zone_number_start=zone_number_start,
                zone_number_end=zone_number_end,
                project=self.project,
                template=self.template,
                filepath=filepath,
            ).process()

        elif is_zone_name_field or is_zone_number_field:
            WriteDocZoneFirstService(
                zone_number_start=zone_number_start,
                zone_number_end=zone_number_end,
                project=self.project,
                template=self.template,
                filepath=filepath,
            ).process()
        elif is_discrepancy_field or is_discrepancy_decimal_field:
            WriteDocDiscrepancyFieldService(
                zone_number_start=zone_number_start,
                zone_number_end=zone_number_end,
                project=self.project,
                template=self.template,
                filepath=filepath,
            ).process()
        else:
            WriteStandardDocService(
                zone_number_start=zone_number_start,
                zone_number_end=zone_number_end,
                project=self.project,
                template=self.template,
                filepath=filepath,
            ).process()

        self._create_event(project=self.project, template=self.template)
        return file.id

    def _get_first_and_last_zone_numbers(self):
        zone_number_start = 1 if self.template.zone_number_start is None else self.template.zone_number_start
        zone_number_end = (
            self.project.zones.count()
            if self.template.zone_number_end is None else
            self.template.zone_number_end
        )

        return zone_number_start, zone_number_end

    def _create_db_file(self):
        """Ф_ция генерит путь к файлу с форматом, создает его в БД, возвращает кортеж путь+файл."""
        date = timezone.now().strftime('%Y/%m/%d')
        dirpath = f'/media/upload/{date}/'
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
        project_title = str(self.project.title).replace('/', '_')
        filepath = f'{dirpath}export_document_{project_title}_{token_urlsafe(4)}.{self.file_format}'
        file = File.objects.create(file=filepath.replace('/media', ''))
        return filepath, file

    def _create_event(self, project: Project, template: Template):
        comment = 'Выгрузка данных; Были выгружены данные со следующими настройками:\r\n\r\nПоля для выгрузки:\r\n'
        template_fieds = template.fields.copy()
        for field in template_fieds:  # noqa: WPS519
            comment += f'{getattr(TemplateExportFieldChoices, field.upper()).label}\r\n'
        comment += '\r\nНастройки:\r\n'
        comment += 'Кодировка "Windows 1251"\r\n'
        comment += f'Разделитель полей: {template.field_separator}\r\n'
        comment += f'Десятичный разделитель: {template.decimal_separator}\r\n'
        Event.objects.create(project=project, title=TitleChoices.EXPORT_PROJECT_DATA, comment=comment)
