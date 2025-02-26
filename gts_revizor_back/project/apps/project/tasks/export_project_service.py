import logging
import os
import shutil
from datetime import datetime

import pandas as pd
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps import app
from apps.document.models import Document
from apps.employee.models import Employee
from apps.event.models import Event
from apps.helpers.services import AbstractService
from apps.product.models import AdditionalProductTitleAttribute, Product, ScannedProduct
from apps.project.models import Project, RMMSettings, TerminalSettings
from apps.task.models import Task
from apps.template.models import Template, TemplateExport
from apps.terminal.models import Terminal
from apps.zone.models import Zone

logger = logging.getLogger('django')
User = get_user_model()


@app.task
def export_project_celery_task_wrapper(host: str, project_id: str):
    return ExportProjectService(host, project_id).process()


class ExportProjectService(AbstractService):
    def __init__(self, host: str, project_id: str):
        self.host = host
        self.project = Project.objects.get(pk=project_id)
        self.manager = self.project.manager

    def process(self, *args, **kwargs):  # noqa: WPS213
        date = timezone.now().strftime('%Y/%m/%d')
        project_title = self.project.title.replace(' ', '_').replace('/', '_')
        dirpath = f'/media/upload/{date}/{self.project.pk}/'
        arch_path = f'/media/upload/{date}/'
        arch_name = f'/backup_{project_title}_{datetime.now().strftime("%Y-%m-%dT%H-%M")}'

        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)

        project = Project.objects.filter(pk=self.project.pk)
        self._save_qs_to_csv(qs=project, csv_file_path=f'{dirpath}project.csv', sep='`')

        project_manager_id = list(project.values_list('manager_id', flat=True))
        project_manager = User.objects.filter(id__in=project_manager_id)
        self._save_qs_to_csv(qs=project_manager, csv_file_path=f'{dirpath}project_manager.csv', sep='`')

        templates = Template.objects.all()
        self._save_qs_to_csv(qs=templates, csv_file_path=f'{dirpath}templates.csv', sep='`')

        export_templates = TemplateExport.objects.all()
        self._save_qs_to_csv(qs=export_templates, csv_file_path=f'{dirpath}export_templates.csv', sep='`')

        employees = Employee.objects.filter(project=self.project)
        self._save_qs_to_csv(qs=employees, csv_file_path=f'{dirpath}employees.csv', sep='`')

        rmm_settings = RMMSettings.objects.filter(project=self.project)
        self._save_qs_to_csv(qs=rmm_settings, csv_file_path=f'{dirpath}rmm_settings.csv', sep='`')

        terminal_settings = TerminalSettings.objects.filter(project=self.project)
        self._save_qs_to_csv(qs=terminal_settings, csv_file_path=f'{dirpath}terminal_settings.csv', sep='`')

        terminals = Terminal.objects.filter(project=self.project)
        self._save_qs_to_csv(qs=terminals, csv_file_path=f'{dirpath}terminals.csv', sep='`')

        products = Product.objects.filter(project=self.project)
        self._save_qs_to_csv(qs=products, csv_file_path=f'{dirpath}products.csv', sep='`')

        scanned_products = ScannedProduct.objects.filter(product__project=self.project)
        self._save_qs_to_csv(qs=scanned_products, csv_file_path=f'{dirpath}scanned_products.csv', sep='`')

        tasks = Task.objects.filter(zone__project=self.project)
        self._save_qs_to_csv(qs=tasks, csv_file_path=f'{dirpath}tasks.csv', sep='`')

        zones = Zone.objects.filter(project=self.project)
        self._save_qs_to_csv(qs=zones, csv_file_path=f'{dirpath}zones.csv', sep='`')

        documents = Document.objects.filter(zone__project=self.project).order_by('created_at')
        self._save_qs_to_csv(qs=documents, csv_file_path=f'{dirpath}documents.csv', sep='`')

        product_title_attrs = AdditionalProductTitleAttribute.objects.filter(project=self.project)
        self._save_qs_to_csv(qs=product_title_attrs, csv_file_path=f'{dirpath}product_title_attrs.csv', sep='`')

        events = Event.objects.filter(project=self.project)
        self._save_qs_to_csv(qs=events, csv_file_path=f'{dirpath}events.csv', sep='`')

        shutil.make_archive(f'{arch_path}{arch_name}', format='zip', root_dir=dirpath)

        return f'{self.host}{arch_path}/{arch_name}.zip'

    @staticmethod
    def _save_qs_to_csv(qs, csv_file_path: str, sep: str):
        df = pd.DataFrame.from_records(qs.values())
        df.to_csv(csv_file_path, sep=sep, header=True, index=False)
