import logging

from django.db import transaction
from rest_framework.exceptions import ValidationError

from api.v1.product.services import GenerateProductsFileService
from apps import app
from apps.document.services import BulkCreateDocumentsService
from apps.employee.services import BulkCreateEmployeesService
from apps.event.models import TitleChoices
from apps.event.services import BulkCreateEventsService, CreateEventService
from apps.file.models import File
from apps.file.services import UnzipService
from apps.helpers.services import AbstractService
from apps.product.services import BulkCreateProductsService, BulkCreateScannedProductsService
from apps.project.models import Project, RMMSettings, TerminalSettings
from apps.task.services import BulkCreateTasksService
from apps.terminal.services import BulkCreateTerminalsService
from apps.user.services import GetOrCreateManagerService
from apps.zone.services import BulkCreateZonesService

logger = logging.getLogger('django')


@app.task
def import_project_new_celery_task_wrapper(file_id: str):
    backup_content = UnzipService(file_id).process()
    project = ImportProjectNewService(backup_content, file_id).process()
    return f'Проект {project} успешно загружен.'


class ImportProjectNewService(AbstractService):
    """Сервис импорта проекта."""

    def __init__(self, backup_content, file_id):
        self.backup_content = backup_content
        self.file = File.objects.get(pk=file_id)

    @transaction.atomic
    def process(self) -> str:  # noqa: WPS213

        manager_content = self.backup_content.get('manager')
        manager = GetOrCreateManagerService(manager_content).process()
        self.backup_content['project']['manager'] = manager
        project_src = self.backup_content.get('project')
        project_title = project_src['title']

        if Project.objects.filter(title=project_title):
            raise ValidationError('Проект уже существует.')

        new_project = Project.objects.create(**self.backup_content.get('project'))
        new_project.rmm_settings.delete()
        new_project.terminal_settings.delete()
        new_project.manager = manager
        new_project.save()

        new_terminal_settings_content = self.backup_content.get('terminal_settings')
        new_terminal_settings_content['project'] = new_project
        TerminalSettings.objects.create(**new_terminal_settings_content)
        new_rmm_settings_content = self.backup_content.get('rmm_settings')
        new_rmm_settings_content['project'] = new_project
        RMMSettings.objects.create(**new_rmm_settings_content)

        employees_content = self.backup_content.get('employees')
        terminals_content = self.backup_content.get('terminals')
        products_content = self.backup_content.get('products')
        zones_content = self.backup_content.get('zones')
        tasks_content = self.backup_content.get('tasks')
        scanned_products_content = self.backup_content.get('scanned_products')
        documents_content = self.backup_content.get('documents')
        events_content = self.backup_content.get('events', [])

        BulkCreateEmployeesService(new_project, employees_content).process()
        BulkCreateTerminalsService(new_project, terminals_content).process()
        BulkCreateProductsService(new_project, products_content).process()
        BulkCreateZonesService(new_project, zones_content).process()
        BulkCreateTasksService(tasks_content).process()
        BulkCreateScannedProductsService(scanned_products_content).process()
        BulkCreateDocumentsService(documents_content).process()
        BulkCreateEventsService(new_project, events_content).process()

        title_event = TitleChoices.IMPORT_PROJECT
        comment = f'Импортирован проект из файла {self.file.file.path.split("/")[-1]}'
        CreateEventService(new_project, title_event, comment).process()

        GenerateProductsFileService(new_project.pk).process()

        return new_project.title
