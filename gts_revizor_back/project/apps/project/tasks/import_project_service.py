import ast
import contextlib
import logging
import os
import shutil

import numpy as np
import pandas as pd
from dateutil.parser import parse
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.exceptions import ValidationError

from api.v1.product.services import GenerateProductsFileService
from apps import app
from apps.document.models import Document
from apps.employee.models import Employee
from apps.event.models import Event
from apps.file.models import File
from apps.helpers.services import AbstractService
from apps.product.models import AdditionalProductTitleAttribute, Product, ScannedProduct
from apps.project.models import Project, RMMSettings, TerminalSettings
from apps.task.models import Task
from apps.terminal.models import Terminal
from apps.zone.models import Zone

logger = logging.getLogger('django')

User = get_user_model()


@app.task
def import_project_celery_task_wrapper(file_id: str):
    serres = ImportProjectService(file_id).process()
    return f'Проект {serres} успешно загружен.'


class ImportProjectService(AbstractService):  # noqa: WPS214
    def __init__(self, file_id: str):
        self.file = File.objects.get(pk=file_id)
        if self.file.file.path.split('.')[-1] != 'zip':
            raise ValidationError('Для загрузки необходим файл формата zip.')

        self.dirpath = os.path.splitext(self.file.file.path)[0]
        if not os.path.isdir(self.dirpath):
            os.makedirs(self.dirpath)

    def process(self) -> str:  # noqa: WPS213, WPS231
        extract_file = self.file.file.path
        extract_dir = self.dirpath
        archive_format = 'zip'
        shutil.unpack_archive(extract_file, extract_dir, archive_format)

        with transaction.atomic():
            project = self._create_project_from_backup()
            self._create_project_manager_from_backup()
            self._create_terminal_settings_from_backup()
            self._create_rmm_settings_from_backup()
            self._create_employees_from_backup()
            self._create_zones_from_backup()
            self._create_terminals_from_backup()
            self._create_products_from_backup()
            self._create_tasks_from_backup()
            self._create_scanned_products_from_backup()
            self._create_documents_from_backup()
            self._create_product_title_attrs_from_backup()
            self._create_events_from_backup()

        GenerateProductsFileService(project.pk).process()

    def _create_project_manager_from_backup(self):
        project_manager_df = pd.read_csv(filepath_or_buffer=f'{self.dirpath}/project_manager.csv', sep='`')
        project_manager_content = project_manager_df.iloc[0]

        return User.objects.get_or_create(
            phone=f'+{project_manager_content["phone"]}',
            defaults={
                'id': project_manager_content['id'],
                'username': project_manager_content['username'],
                'first_name': project_manager_content['first_name'],
                'middle_name': project_manager_content['middle_name'],
                'last_name': project_manager_content['last_name'],
            },
        )

    def _create_project_from_backup(self) -> Project:
        project_df = pd.read_csv(filepath_or_buffer=f'{self.dirpath}/project.csv', sep='`')
        project_content = project_df.iloc[0]

        project_created_at = project_content['created_at']

        user, _ = self._create_project_manager_from_backup()

        project = Project.objects.create(
            id=project_content['id'],
            created_at=project_created_at,
            title=project_content['title'],
            address=project_content['address'],
            manager_id=user.id,
            accounting_without_yk=project_content['accounting_without_yk'],
            auto_assign_enbale=project_content['auto_assign_enbale'],
        )

        project.created_at = project_created_at
        project.rmm_settings.delete()
        project.terminal_settings.delete()
        project.save()

        return project

    def _create_terminal_settings_from_backup(self):
        terminal_settings_df = pd.read_csv(filepath_or_buffer=f'{self.dirpath}/terminal_settings.csv', sep='`')
        terminal_settings_content = terminal_settings_df.iloc[0]

        TerminalSettings.objects.create(**terminal_settings_content)

    def _create_rmm_settings_from_backup(self):
        rmm_settings_df = pd.read_csv(filepath_or_buffer=f'{self.dirpath}/rmm_settings.csv', sep='`')
        rmm_settings_content = rmm_settings_df.iloc[0]

        RMMSettings.objects.create(**rmm_settings_content)

    def _create_employees_from_backup(self):
        employees_df = pd.read_csv(filepath_or_buffer=f'{self.dirpath}/employees.csv', sep='`')
        employees_df['serial_number'] = employees_df['serial_number'].replace(np.nan, None)

        employees = [
            Employee(
                id=row['id'],
                project_id=row['project_id'],
                username=row['username'],
                serial_number=row['serial_number'],
                roles=ast.literal_eval(row['roles']),
                is_deleted=row['is_deleted'],
                is_auto_assignment=row['is_auto_assignment'],
            )
            for _, row in employees_df.iterrows()
        ]

        Employee.objects.bulk_create(employees)

    def _create_zones_from_backup(self):
        zones_df = pd.read_csv(filepath_or_buffer=f'{self.dirpath}/zones.csv', sep='`')
        zones_df['storage_name'] = zones_df['storage_name'].replace(np.nan, '')

        zones = [Zone(**record) for record in zones_df.to_dict(orient='records')]

        Zone.objects.bulk_create(zones)

    def _create_terminals_from_backup(self):
        terminals_df = pd.read_csv(filepath_or_buffer=f'{self.dirpath}/terminals.csv', sep='`')
        terminals_df['mac_address'] = terminals_df['mac_address'].replace(np.nan, '')
        terminals_df['device_model'] = terminals_df['device_model'].replace(np.nan, '')

        terminals = [
            Terminal(
                id=row['id'],
                project_id=row['project_id'],
                employee_id=self._check_dataframe_field_to_nan(row['employee_id']),
                number=row['number'],
                ip_address=row['ip_address'],
                db_loading=row['db_loading'],
                last_connect=self._convert_str_to_datetime(row['last_connect']),
                mac_address=row['mac_address'],
                device_model=row['device_model'],
            )
            for _, row in terminals_df.iterrows()
        ]

        Terminal.objects.bulk_create(terminals)

    def _create_products_from_backup(self):
        products_df = pd.read_csv(filepath_or_buffer=f'{self.dirpath}/products.csv', sep='`')

        products_df['qr_code'] = products_df['qr_code'].replace(np.nan, '')
        products_df['am'] = products_df['am'].replace(np.nan, '')
        products_df['dm'] = products_df['dm'].replace(np.nan, '')
        products_df['size'] = products_df['size'].replace(np.nan, '')
        products_df['store_number'] = products_df['store_number'].replace(np.nan, None)

        products = [Product(**record) for record in products_df.to_dict(orient='records')]

        Product.objects.bulk_create(products)

    def _create_tasks_from_backup(self):
        tasks_df = pd.read_csv(filepath_or_buffer=f'{self.dirpath}/tasks.csv', sep='`')

        tasks = [
            Task(
                id=row['id'],
                zone_id=row['zone_id'],
                employee_id=row['employee_id'],
                type=row['type'],
                status=row['status'],
                result=row['result'],
                terminal_id=self._check_dataframe_field_to_nan(row['terminal_id']),
            )
            for _, row in tasks_df.iterrows()
        ]

        Task.objects.bulk_create(tasks)

    def _create_scanned_products_from_backup(self):
        scanned_products_df = pd.read_csv(filepath_or_buffer=f'{self.dirpath}/scanned_products.csv', sep='`')

        scanned_products = [
            ScannedProduct(
                id=row['id'],
                product_id=row['product_id'],
                task_id=row['task_id'],
                amount=row['amount'],
                scanned_time=self._convert_str_to_datetime(row['scanned_time']),
                added_by_product_code=row['added_by_product_code'],
                added_by_qr_code=row['added_by_qr_code'],
                is_weight=row['is_weight'],
                dm=row['dm'],
            )
            for _, row in scanned_products_df.iterrows()
        ]

        ScannedProduct.objects.bulk_create(scanned_products)

    def _create_documents_from_backup(self):
        documents_df = pd.read_csv(filepath_or_buffer=f'{self.dirpath}/documents.csv', sep='`')

        documents = [
            Document(
                id=row['id'],
                fake_id=row['fake_id'],
                employee_id=self._check_dataframe_field_to_nan(row['employee_id']),
                zone_id=self._check_dataframe_field_to_nan(row['zone_id']),
                status=row['status'],
                start_audit_date=self._convert_str_to_datetime(row['start_audit_date']),
                end_audit_date=self._convert_str_to_datetime(row['end_audit_date']),
                tsd_number=row['tsd_number'],
                terminal_id=self._check_dataframe_field_to_nan(row['terminal_id']),
                suspicious=row['suspicious'],
                color=row['color'],
                prev_color=row['prev_color'],
                color_changed=row['color_changed'],
                counter_scan_task_id=self._check_dataframe_field_to_nan(row['counter_scan_task_id']),
                controller_task_id=self._check_dataframe_field_to_nan(row['controller_task_id']),
                auditor_task_id=self._check_dataframe_field_to_nan(row['auditor_task_id']),
                auditor_controller_task_id=self._check_dataframe_field_to_nan(row['auditor_controller_task_id']),
                auditor_external_task_id=self._check_dataframe_field_to_nan(row['auditor_external_task_id']),
                storage_task_id=self._check_dataframe_field_to_nan(row['storage_task_id']),
                is_replace_specification=row['is_replace_specification'],
            )
            for _, row in documents_df.iterrows()
        ]

        Document.objects.bulk_create(documents)

    def _create_product_title_attrs_from_backup(self):
        try:
            product_title_attrs_df = pd.read_csv(filepath_or_buffer=f'{self.dirpath}/product_title_attrs.csv', sep='`')
        except pd.errors.EmptyDataError:
            return

        product_title_attrs = [
            AdditionalProductTitleAttribute(
                id=row['id'],
                project_id=row['project_id'],
                product_id=row['product_id'],
                content=row['content'],
                is_hidden=row['is_hidden'],
            )
            for _, row in product_title_attrs_df.iterrows()
        ]

        AdditionalProductTitleAttribute.objects.bulk_create(product_title_attrs)

    def _create_events_from_backup(self):
        events_df = pd.read_csv(filepath_or_buffer=f'{self.dirpath}/events.csv', sep='`')

        events = [
            Event(
                id=row['id'],
                fake_id=row['fake_id'],
                project_id=row['project_id'],
                title=row['title'],
                comment=row['comment'],
            )
            for _, row in events_df.iterrows()
        ]

        Event.objects.bulk_create(events)

    @staticmethod
    def _check_dataframe_field_to_nan(dataframe_field):
        return None if isinstance(dataframe_field, float) else dataframe_field

    @staticmethod
    def _convert_str_to_datetime(string_date: str):
        with contextlib.suppress(ValueError, TypeError):
            return parse(string_date)
