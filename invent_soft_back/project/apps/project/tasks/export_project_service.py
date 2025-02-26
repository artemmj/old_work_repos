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
from apps.product.models import AdditionalProductTitleAttribute, Product
from apps.project.models import Project, RMMSettings, TerminalSettings
from apps.terminal.models import Terminal
from apps.zone.models import Zone

from .serializers import (  # noqa: WPS235
    DocumentBackupSerializer,
    EmployeeBackupSerializer,
    EventBackupSerializer,
    ProductBackupSerializer,
    ProjectBackupSerializer,
    RMMSettingsBackupSerializer,
    TerminalBackupSerializer,
    TerminalSettingsBackupSerializer,
    UserBackupSerializer,
    ZoneBackupSerializer,
)

logger = logging.getLogger('django')


@app.task
def export_project_celery_task_wrapper(host: str, project_id: str):
    return ExportProjectService(host, project_id).process()


class ExportProjectService(AbstractService):
    def __init__(self, host: str, project_id: str):
        self.host = host
        self.project = Project.objects.get(pk=project_id)
        self.manager = self.project.manager

    def process(self, *args, **kwargs):
        rmm_settings_obj = RMMSettings.objects.get(project=self.project)
        terminal_settings_obj = TerminalSettings.objects.get(project=self.project)

        employees = Employee.objects.filter(project=self.project)
        terminals = Terminal.objects.filter(project=self.project)
        products = Product.objects.filter(project=self.project)
        zones = Zone.objects.filter(project=self.project)
        documents = Document.objects.filter(zone__project=self.project)
        events = Event.objects.filter(project=self.project)
        product_title_attrs = AdditionalProductTitleAttribute.objects.filter(project=self.project)

        data = {
            'project': ProjectBackupSerializer(self.project).data,
            'manager': UserBackupSerializer(self.project.manager).data,
            'terminal_settigns': TerminalSettingsBackupSerializer(terminal_settings_obj).data,
            'rmm_settings': RMMSettingsBackupSerializer(rmm_settings_obj).data,
            'employees': EmployeeBackupSerializer(employees, many=True).data,
            'terminals': TerminalBackupSerializer(terminals, many=True).data,
            'products': ProductBackupSerializer(products, many=True).data,
            'zones': ZoneBackupSerializer(zones, many=True).data,
            'documents': DocumentBackupSerializer(documents, many=True).data,
            'events': EventBackupSerializer(events, many=True).data,
            'product_title_attrs': AdditionalProductTitleAttrBackupSerializer(product_title_attrs, many=True).data,
        }
        with open('data.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False)

        date = timezone.now().strftime('%Y/%m/%d')
        dirpath = f'/media/upload/{date}/{self.project.pk}/'
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
        arch_name = f'backup_{self.project.title.replace(" ", "_")}_{datetime.now().strftime("%Y-%m-%dT%H-%M")}.zip'
        with zipfile.ZipFile(f'{dirpath}/{arch_name}', 'w') as zipper:
            zipper.write('data.json', compress_type=zipfile.ZIP_STORED)
        os.remove('data.json')
        return f'{self.host}{dirpath}/{arch_name}'
