import logging
import os
from datetime import datetime
from typing import Dict, List
from uuid import uuid4, uuid5

from celery import current_task
from django.db import connection

from apps import app
from apps.helpers.services import AbstractService
from apps.product.models import FileOfProjectProducts, Product, ScannedProduct
from apps.project.models import Project

CHUNK_SIZE = 30000

logger = logging.getLogger('django')


@app.task
def delete_products_celery_wrapper(serializer_data: Dict):
    """Обертка для асинхронного удаления товаров."""
    return DeleteProjectProductsService(serializer_data=serializer_data).process()


class DeleteProjectProductsService(AbstractService):  # noqa: WPS338
    def __init__(self, serializer_data: Dict):
        self.project = Project.objects.get(id=serializer_data.get('project'))
        self.params = serializer_data.get('params')

    def _chunks(self, lst, n):
        """Получение последовательных фрагментов размером n из lst."""  # noqa: DAR301
        for i in range(0, len(lst), n):  # noqa: WPS526
            yield lst[i:i + n]

    def _make_and_execute_queries(self, chunk: List[str]):
        cursor = connection.cursor()

        delete_query = 'BEGIN;\r\n'
        logs_query = 'BEGIN;\r\n'

        for product_id in chunk:
            delete_query += f"DELETE FROM product_product WHERE id = \'{product_id}\';\r\n"

            id = str(uuid5(uuid4(), str(uuid4)))  # noqa: WPS125
            created_at = datetime.now()
            logs_query += f""" INSERT INTO changelog_changelog
                (id, created_at, model, record_id, action_on_model, changed_data, project_id)
                VALUES
                ('{id}', '{created_at}', 'product', '{product_id}', 'delete', '{{}}', '{self.project.pk}');\r\n
            """

        delete_query += 'COMMIT;'
        logs_query += 'COMMIT;'

        cursor.execute(delete_query)
        cursor.execute(logs_query)

    def process(self):  # noqa: WPS231
        if 'delete_all' not in self.params:
            if 'delete_prices' in self.params:
                Product.objects.filter(project=self.project).update(price=0)
            if 'delete_remainders' in self.params:
                Product.objects.filter(project=self.project).update(remainder=0)
            return

        # Сначала необходимо проставить всем отсканированным товарам Неизвестный товар, сохранив штрихкод
        for scan_prd in ScannedProduct.objects.filter(product__project=self.project):
            unknown_prd, _ = Product.objects.get_or_create(
                project=self.project,
                title='Неизвестный товар',
                barcode=scan_prd.product.barcode,
                vendor_code=f'art_{scan_prd.product.barcode}',
            )
            scan_prd.product = unknown_prd
            scan_prd.save()

        delete_pks = list(
            Product.objects.filter(
                project=self.project,
            ).exclude(
                title='Неизвестный товар',
            ).values_list(
                'pk', flat=True,
            ),
        )

        delete_counter = CHUNK_SIZE
        for chunk in self._chunks(lst=delete_pks, n=CHUNK_SIZE):
            self._make_and_execute_queries(chunk=chunk)
            current_task.update_state(
                state='PENDING',
                meta={
                    'current': delete_counter,
                    'total': len(delete_pks),
                    'percent': int(delete_counter / (len(delete_pks) / 100)),
                },
            )
            delete_counter += CHUNK_SIZE

        try:
            file_of_products = FileOfProjectProducts.objects.get(project=self.project)
        except FileOfProjectProducts.DoesNotExist:
            pass  # noqa: WPS420
        else:
            path = file_of_products.products_file
            file_of_products.delete()
            try:  # noqa: WPS505
                os.remove(path)
            except FileNotFoundError:
                pass  # noqa: WPS420

        return  # noqa: WPS324
