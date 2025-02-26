import json
import logging
import os
import zipfile

from rest_framework.exceptions import ValidationError

from apps import app
from apps.document.models import Document
from apps.employee.models import Employee
from apps.event.models import Event, TitleChoices
from apps.file.models import File
from apps.helpers.services import AbstractService
from apps.product.models import Product, ScannedProduct
from apps.project.models import Project, RMMSettings, TerminalSettings, User
from apps.task.models import Task
from apps.terminal.models import Terminal
from apps.zone.models import Zone

logger = logging.getLogger('django')


@app.task
def import_project_celery_task_wrapper(file_id: str):
    serres = ImportProjectService(file_id).process()
    return f'Проект {serres} успешно загружен.'


class ImportProjectService(AbstractService):
    def __init__(self, file_id: str):
        self.file = File.objects.get(pk=file_id)
        if self.file.file.path.split('.')[-1] != 'zip':
            raise ValidationError('Для загрузки необходим файл формата zip.')

        self.dirpath = os.path.splitext(self.file.file.path)[0]
        if not os.path.isdir(self.dirpath):
            os.makedirs(self.dirpath)

    def process(self) -> str:  # noqa: WPS213, WPS231
        zip = zipfile.ZipFile(self.file.file.path)  # noqa: WPS125
        for zip_file in zip.namelist():
            zip.extract(zip_file, self.dirpath)
        with open(f'{self.dirpath}/data.json') as f:
            data = json.load(f)

        ids_maping = {
            'employees': {},
            'terminals': {},
            'products': {},
            'zones': {},
            'tasks': {},
            'scanned_products': {},
            'documents': {},
        }

        manager, _ = User.objects.get_or_create(
            phone=data['manager']['phone'],
            defaults={
                'username': data['manager']['username'],
                'first_name': data['manager']['first_name'],
                'middle_name': data['manager']['middle_name'],
                'last_name': data['manager']['last_name'],
            },
        )
        data['project']['manager'] = manager
        new_project = Project.objects.create(**data.get('project'))
        new_project.rmm_settings.delete()
        new_project.terminal_settings.delete()
        new_project.manager = manager
        new_project.save()

        new_terminal_settings_data = data.get('terminal_settigns')
        new_terminal_settings_data['project'] = new_project
        TerminalSettings.objects.create(**new_terminal_settings_data)
        new_rmm_settings_data = data.get('rmm_settings')
        new_rmm_settings_data['project'] = new_project
        RMMSettings.objects.create(**new_rmm_settings_data)

        for src_employee in data.get('employees'):
            src_employee['project'] = new_project
            orig_id = src_employee.pop('id')
            new_employee = Employee.objects.create(**src_employee)
            ids_maping['employees'][orig_id] = new_employee.pk

        for src_terminal in data.get('terminals'):
            src_terminal['project'] = new_project
            orig_id = src_terminal.pop('id')
            new_terminal = Terminal.objects.create(**src_terminal)
            ids_maping['terminals'][orig_id] = new_terminal.pk

        for src_product in data.get('products'):
            src_product['project'] = new_project
            orig_id = src_product.pop('id')
            new_product = Product.objects.create(**src_product)
            ids_maping['products'][orig_id] = new_product.pk

        for src_zone in data.get('zones', []):
            src_zone_tasks = src_zone.pop('tasks')
            src_zone['project'] = new_project
            orig_id = src_zone.pop('id')
            new_zone = Zone.objects.create(**src_zone)
            ids_maping['zones'][orig_id] = new_zone.pk
            for src_task in src_zone_tasks:
                src_task['zone'] = new_zone
                src_task['employee'] = Employee.objects.get(pk=ids_maping['employees'][src_task.get('employee')])
                if src_task.get('terminal'):
                    src_task['terminal'] = Terminal.objects.get(pk=ids_maping['terminals'][src_task.get('terminal')])
                src_scanned_products = src_task.pop('scanned_products')
                orig_id = src_task.pop('id')
                new_task = Task.objects.create(**src_task)
                ids_maping['tasks'][orig_id] = new_task.pk  # noqa: WPS204
                for src_scanned_product in src_scanned_products:
                    src_scanned_product['product'] = Product.objects.get(
                        pk=ids_maping['products'][src_scanned_product.pop('product')],
                    )
                    src_scanned_product['task'] = new_task
                    ScannedProduct.objects.create(**src_scanned_product)

        for src_document in data.get('documents'):
            src_document['employee'] = Employee.objects.get(pk=ids_maping['employees'][src_document.get('employee')])
            src_document['zone'] = Zone.objects.get(pk=ids_maping['zones'][src_document.get('zone')])
            if src_document.get('terminal'):
                src_document['terminal'] = Terminal.objects.get(
                    pk=ids_maping['terminals'][src_document.get('terminal')],
                )
            if src_document['counter_scan_task']:
                src_document['counter_scan_task'] = Task.objects.get(
                    pk=ids_maping['tasks'][src_document.get('counter_scan_task')],
                )
            if src_document['controller_task']:
                src_document['controller_task'] = Task.objects.get(
                    pk=ids_maping['tasks'][src_document.get('controller_task')],
                )
            if src_document['auditor_task']:
                src_document['auditor_task'] = Task.objects.get(
                    pk=ids_maping['tasks'][src_document.get('auditor_task')],
                )
            if src_document['auditor_controller_task']:
                src_document['auditor_controller_task'] = Task.objects.get(
                    pk=ids_maping['tasks'][src_document.get('auditor_controller_task')],
                )
            if src_document['storage_task']:
                src_document['storage_task'] = Task.objects.get(
                    pk=ids_maping['tasks'][src_document.get('storage_task')],
                )
            real_fake_id = src_document.pop('fake_id')
            new_document = Document.objects.create(**src_document)
            new_document.fake_id = real_fake_id
            new_document.save()

        for src_event in data.get('events', []):
            src_event['project'] = new_project
            Event.objects.create(**src_event)

        Event.objects.create(
            project=new_project,
            title=TitleChoices.IMPORT_PROJECT,
            comment=f'Импортирован проект из файла {self.file.file.path.split("/")[-1]}',
        )

        return new_project.title
