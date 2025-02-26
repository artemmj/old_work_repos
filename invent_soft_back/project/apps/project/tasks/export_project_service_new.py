import json
import logging
import os
import zipfile
from datetime import datetime

from django.utils import timezone

from api.v1.product.serializers import AdditionalProductTitleAttrBackupSerializer
from apps import app
from apps.document.models import Document
from apps.employee.models import Employee
from apps.event.models import Event
from apps.helpers.services import AbstractService
from apps.product.models import AdditionalProductTitleAttribute, Product, ScannedProduct
from apps.project.models import Project, RMMSettings, TerminalSettings
from apps.task.models import Task
from apps.terminal.models import Terminal
from apps.zone.models import Zone

from .serializers_new import (  # noqa: WPS235
    DocumentBackupSerializer,
    EmployeeBackupSerializer,
    EventBackupSerializer,
    ProductBackupSerializer,
    ProjectBackupSerializer,
    RMMSettingsBackupSerializer,
    ScannedProductSerializer,
    TaskReadSerializer,
    TerminalBackupSerializer,
    TerminalSettingsBackupSerializer,
    UserBackupSerializer,
    ZoneBackupSerializer,
)

logger = logging.getLogger('django')


@app.task
def export_project_new_celery_task_wrapper(host: str, project_id: str):
    return ExportProjectNewService(host, project_id).process()


class ExportProjectNewService(AbstractService):
    def __init__(self, host: str, project_id: str):
        self.host = host
        self.project = Project.objects.get(pk=project_id)
        self.manager = self.project.manager

    def process(self, *args, **kwargs):
        rmm_settings = RMMSettings.objects.get(project=self.project)
        terminal_settings = TerminalSettings.objects.get(project=self.project)

        employees = Employee.objects.filter(project=self.project)
        terminals = Terminal.objects.filter(project=self.project)
        products = Product.objects.filter(project=self.project)
        zones = Zone.objects.filter(project=self.project)
        tasks = Task.objects.filter(zone__project=self.project)
        scanned_products = ScannedProduct.objects.filter(task__zone__project=self.project)
        documents = Document.objects.filter(zone__project=self.project)
        events = Event.objects.filter(project=self.project)
        product_title_attrs = AdditionalProductTitleAttribute.objects.filter(project=self.project)

        project_content = {
            'project': ProjectBackupSerializer(self.project).data,
            'manager': UserBackupSerializer(self.project.manager).data,
            'terminal_settings': TerminalSettingsBackupSerializer(terminal_settings).data,
            'rmm_settings': RMMSettingsBackupSerializer(rmm_settings).data,
            'employees': EmployeeBackupSerializer(employees, many=True).data,
            'terminals': TerminalBackupSerializer(terminals, many=True).data,
            'products': ProductBackupSerializer(products, many=True).data,
            'zones': ZoneBackupSerializer(zones, many=True).data,
            'tasks': TaskReadSerializer(tasks, many=True).data,
            'scanned_products': ScannedProductSerializer(scanned_products, many=True).data,
            'documents': DocumentBackupSerializer(documents, many=True).data,
            'events': EventBackupSerializer(events, many=True).data,
            'product_title_attrs': AdditionalProductTitleAttrBackupSerializer(product_title_attrs, many=True).data,
        }

        with open('data.json', 'w') as f:
            json.dump(project_content, f, ensure_ascii=False)

        date = timezone.now().strftime('%Y/%m/%d')
        dir_path = f'/media/upload/{date}/{self.project.pk}/'
        os.makedirs(dir_path, exist_ok=True)
        arch_name = f'backup_{self.project.title.replace(" ", "_")}_{datetime.now().strftime("%Y-%m-%dT%H-%M")}.zip'

        with zipfile.ZipFile(f'{dir_path}/{arch_name}', 'w') as zipper:
            zipper.write('data.json', compress_type=zipfile.ZIP_STORED)
        os.remove('data.json')

        return f'{self.host}{dir_path}/{arch_name}'
