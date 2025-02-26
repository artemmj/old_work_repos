import csv
import logging
import sys
from contextlib import suppress
from datetime import datetime
from uuid import uuid4, uuid5

from celery import current_task
from django.db import connection
from rest_framework.exceptions import ValidationError

from api.v1.product.services import GenerateProductsFileService, GetProductTitleAttrsService
from apps import app
from apps.changelog.tasks import UpdateLogsAfterImportProductsService
from apps.event.models import Event, TitleChoices
from apps.file.models import File
from apps.helpers.services import AbstractService
from apps.product.models import AdditionalProductTitleAttribute, Product
from apps.project.models import Project
from apps.template.models import Template
from apps.template.models.template_choices import TemplateFieldChoices

logger = logging.getLogger('django')

CHUNK_SIZE = 2500


@app.task()
def import_products_celery_wrapper(serializer_data: dict):
    """Обертка для асинхронной загрузки товаров."""
    return ImportProductsService(serializer_data).process()


class ImportProductsService(AbstractService):  # noqa: WPS338
    """Сервис для импорта товаров из файла по шаблону."""

    def __init__(self, serializer_data: dict) -> None:
        self.products_file: File = File.objects.get(id=serializer_data['file'])
        self.project: Project = Project.objects.get(pk=serializer_data['project'])
        self.template: Template = Template.objects.get(id=serializer_data['template'])

        if self.products_file.file.path.split('.')[-1] not in ('csv', 'txt'):  # noqa: WPS510
            raise ValidationError('Для загрузки необходим файл формата csv или txt.')

    def _chunks(self, lst, n):
        """Получение последовательных фрагментов размером n из lst."""  # noqa: DAR301
        for i in range(0, len(lst), n):  # noqa: WPS526
            yield lst[i:i + n]

    def _load_memory_data(self):  # noqa: WPS231
        """Записать данные из файла в память, плюс некоторая логика по товарам Х5."""
        memory_data = []
        with open(self.products_file.file.path, newline='', encoding='windows-1251') as ifile:
            reader = csv.reader(ifile, delimiter=self.template.field_separator)
            for line in reader:
                if not line or not line[0]:
                    continue

                raw_create_data = dict(zip(self.template.fields, line))

                create_data_without_not_download_fields = {
                    key: value
                    for key, value in raw_create_data.items()
                    if 'download_' not in key
                }

                create_data_with_additional_title_attributes = {
                    key: value
                    for key, value in create_data_without_not_download_fields.items()
                    if 'additional_title' in key
                }

                create_data_with_hidden_title_attrs = {
                    key: value
                    for key, value in create_data_without_not_download_fields.items()
                    if 'hidden_title_attr' in key
                }

                create_data = {
                    key: value
                    for key, value in create_data_without_not_download_fields.items()
                    if not any(
                        title_attr in key
                        for title_attr in {'additional_title', 'hidden_title_attr'}  # noqa: WPS335
                    )
                }

                create_data['additional_title_attrs'] = create_data_with_additional_title_attributes
                create_data['hidden_title_attrs'] = create_data_with_hidden_title_attrs

                create_data['title'] = create_data['title'].strip()
                # Дополнительно, если есть поле measure сложить его со строкой названия товара
                if 'measure' in create_data:
                    create_data['title'] = f'{create_data["title"]}, {create_data.pop("measure")}'  # noqa: WPS204
                # или если есть поле name_sk поступить ровно так же
                if 'name_sk' in create_data:
                    create_data['title'] = f'{create_data["title"]}, {create_data.pop("name_sk")}'

                if 'price' in create_data:
                    create_data['price'] = create_data['price'].replace(' ', '')

                create_data['title'] = create_data['title'].replace("\'", ' ')
                create_data['project_id'] = str(self.project.pk)

                # Если в шаблоне товар Х5, товар может содержать
                # несколько ШК в одной строке. Каждый ШК - отдельный товар
                if 'barcode_x5' in self.template.fields:
                    for barcode in create_data.pop('barcode_x5').split('-'):
                        create_data['barcode'] = barcode
                        memory_data.append(create_data.copy())
                else:
                    memory_data.append(create_data)

        memory_size = sys.getsizeof(memory_data) / 1000
        logger.info(
            f'Начинаю запись товаров, {len(memory_data)} записей ({memory_size} кБайт) ...',
        )
        return memory_data

    @staticmethod
    def _prepare_raw_sql_for_updating_title_attrs(
        new_title_attrs,
        old_title_attrs,
        is_hidden: bool,
    ):
        """Подготавливает SQL запрос для обновления дополнительных аттрибутов названия товара.

        Args:
            old_title_attrs: старые значения аттрибутов товара
            new_title_attrs: новые значения аттрибутов товара
            is_hidden: скрытый или нет

        Returns:
            str: SQL запрос для обновления дополнительных аттрибутов названия товара
        """
        sql_queries = ''
        title_attrs_table_name = AdditionalProductTitleAttribute.objects.model._meta.db_table

        new_title_attrs_values = (
            title_attr
            for title_attr in new_title_attrs.values()
        )
        for old_title_attr in old_title_attrs:
            with suppress(StopIteration):
                attrs_expr = f"content = '{next(new_title_attrs_values)}', is_hidden = {is_hidden}"
                sql_queries += f"UPDATE {title_attrs_table_name} SET {attrs_expr} WHERE id=\'{old_title_attr.id}\';\r\n"
        return sql_queries

    @staticmethod
    def _prepare_raw_sql_for_creating_title_attrs(
        project: Project,
        product_id,
        title_attr_value: str,
        is_hidden: bool,
    ) -> str:
        """Подготавливает SQL запрос для создания дополнительного аттрибута названия товара.

        Args:
            title_attr_value: значение аттрибута
            is_hidden: скрытый или нет

        Returns:
            str: SQL запрос для создания дополнительного аттрибута названия товара
        """
        title_attrs_table_name = AdditionalProductTitleAttribute.objects.model._meta.db_table
        attrs_keys = str(('id', 'project_id', 'product_id', 'content', 'is_hidden')).replace("\'", '')
        attrs_values = (uuid4(), project.id, product_id, title_attr_value, is_hidden)
        return f'INSERT INTO {title_attrs_table_name} {attrs_keys} VALUES {attrs_values};\r\n'

    def process(self, *args, **kwargs):  # noqa: WPS213, WPS231
        """Точка входа."""  # noqa: DAR401
        # Проверить соответствие полей шаблона и полей в файле
        with open(self.products_file.file.path, newline='', encoding='windows-1251') as ifile:
            for row in csv.reader(ifile, delimiter=self.template.field_separator):
                if len(row) != len(self.template.fields):
                    raise ValidationError(
                        'Не совпадает количество полей в файле и полей в шаблоне. Проверьте файл и шаблон.',
                    )
                break

        # Необходимо хранить информацию о записанных/обновленных товарах
        created_products, updated_products = [], []

        # Генерим удобный массив словарей, по которому дальше работаем
        memory_data = self._load_memory_data()
        memory_data_len = len(memory_data)
        counter = 0

        current_task.update_state(
            state='PENDING', meta={'current': 1, 'total': memory_data_len, 'percent': 1},
        )
        start_time = datetime.now()
        for chunk in self._chunks(memory_data, CHUNK_SIZE):
            sql_query_list = 'BEGIN;\r\n'
            for product_data in chunk:
                exist_products = Product.objects.filter(project=self.project, barcode=product_data['barcode'])
                additional_title_attrs_from_request = product_data.pop('additional_title_attrs')
                hidden_title_attrs_from_request = product_data.pop('hidden_title_attrs')
                if exist_products:
                    # Обновить все найденные c таким ШК товары
                    for product in exist_products:
                        additional_title_attrs_from_db = GetProductTitleAttrsService(
                            product_id=product.id,
                            project_id=self.project.id,
                            is_hidden=False,
                        ).process()
                        hidden_title_attrs_from_db = GetProductTitleAttrsService(
                            product_id=product.id,
                            project_id=self.project.id,
                            is_hidden=True,
                        ).process()
                        if 'id' in product_data:
                            product_data.pop('id')
                        expr = ''
                        for key, value in product_data.items():
                            if key == 'price':
                                value = value.replace(',', '.')
                            if key == 'remainder':
                                value = value.replace(',', '.')
                            expr += f"{key} = '{value}', "
                        sql_query_list += f"UPDATE product_product SET {expr[:-2]} WHERE id = \'{product.pk}\';\r\n"
                        product_data['id'] = product.pk
                        updated_products.append(product_data)

                        if additional_title_attrs_from_request:
                            sql_query_list += self._prepare_raw_sql_for_updating_title_attrs(
                                new_title_attrs=additional_title_attrs_from_request,
                                old_title_attrs=additional_title_attrs_from_db,
                                is_hidden=False,
                            )

                        if hidden_title_attrs_from_request:
                            sql_query_list += self._prepare_raw_sql_for_updating_title_attrs(
                                new_title_attrs=hidden_title_attrs_from_request,
                                old_title_attrs=hidden_title_attrs_from_db,
                                is_hidden=True,
                            )
                else:
                    price = product_data.get('price').replace(',', '.') if product_data.get('price') else 0
                    remainder = product_data.get('remainder').replace(',', '.') if product_data.get('remainder') else 0
                    # Записать новый товар в лист sql выражений
                    product_id = str(uuid5(uuid4(), str(uuid4())))
                    new_product_data = {  # noqa: WPS122
                        'id': product_id,
                        'project_id': str(self.project.pk),
                        'barcode': product_data.get('barcode', None),
                        'title': product_data.get('title', None),
                        'vendor_code': product_data.get('vendor_code', None),
                        'price': price,
                        'remainder': remainder,
                    }

                    dm = product_data.get('dm', None)
                    if dm:
                        new_product_data['dm'] = dm
                    store_number = product_data.get('store_number', None)
                    if store_number:
                        new_product_data['store_number'] = store_number

                    keys = str(tuple(new_product_data.keys())).replace("\'", '')
                    values = tuple(new_product_data.values())
                    sql_query_list += f'INSERT INTO product_product {keys} VALUES {values};\r\n'
                    created_products.append(new_product_data)

                    if additional_title_attrs_from_request:
                        for additional_title_attr_value in additional_title_attrs_from_request.values():  # noqa: WPS519
                            sql_query_list += self._prepare_raw_sql_for_creating_title_attrs(
                                project=self.project,
                                product_id=product_id,
                                title_attr_value=additional_title_attr_value,
                                is_hidden=False,
                            )

                    if hidden_title_attrs_from_request:
                        for new_hidden_title_attr_value in hidden_title_attrs_from_request.values():  # noqa: WPS519
                            sql_query_list += self._prepare_raw_sql_for_creating_title_attrs(
                                project=self.project,
                                product_id=product_id,
                                title_attr_value=new_hidden_title_attr_value,
                                is_hidden=True,
                            )

            sql_query_list += 'COMMIT;\r\n'
            cursor = connection.cursor()
            cursor.execute(sql_query_list)
            counter += len(chunk)

            logger.info(f'Чанк успешно записан в БД ... ({datetime.now() - start_time}) ({counter}/{memory_data_len})')
            current_task.update_state(
                state='PENDING',
                meta={
                    'current': counter,
                    'total': memory_data_len,
                    'percent': int(counter / (memory_data_len / 100) - 1),
                },
            )
            sql_query_list = ''

        if 'vendor_code' in self.template.fields:
            Event.objects.create(
                project=self.project,
                title=TitleChoices.UPDATE_ARTICLES,
                comment=f'Обновлены артикулы в проекте {self.project}',
            )

        if 'remainder' in self.template.fields or 'remainder_2' in self.template.fields:
            Event.objects.create(
                project=self.project,
                title=TitleChoices.UPDATE_REMAINDER,
                comment=f'Обновлены остатки в проекте {self.project}',
            )

        current_task.update_state(
            state='PENDING',
            meta={'current': counter, 'total': memory_data_len, 'percent': 97},
        )
        # Записать логи всех изменений
        UpdateLogsAfterImportProductsService(created_products, updated_products).process()

        current_task.update_state(
            state='PENDING',
            meta={'current': counter, 'total': memory_data_len, 'percent': 98},
        )
        # Сгенерировать новый файл с товарами, старый удалить
        GenerateProductsFileService(self.project.pk).process()
