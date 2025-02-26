import logging
from datetime import datetime
from typing import Dict, List
from uuid import uuid4, uuid5

from django.db import connection

from apps import app
from apps.helpers.services import AbstractService

logger = logging.getLogger('django')

CHUNK_SIZE = 30000


@app.task
def update_change_logs_after_import_celery_wrapper(created_data, updated_data):  # noqa: WPS118
    return UpdateLogsAfterImportProductsService(created_data, updated_data).process()


class UpdateLogsAfterImportProductsService(AbstractService):  # noqa: WPS338
    def __init__(self, created_data: List[Dict], updated_data: List[Dict]) -> None:  # noqa: D107
        self.created_data = created_data
        self.updated_data = updated_data

    def _chunks(self, lst, n):
        """Получение последовательных фрагментов размером n из lst."""  # noqa: DAR301
        for i in range(0, len(lst), n):  # noqa: WPS526
            yield lst[i:i + n]

    def _write_chunk(self, chunk: List[Dict], created: bool):  # noqa: WPS210
        cursor = connection.cursor()
        sql_create = 'BEGIN;\r\n'

        for product_data in chunk:
            id = str(uuid5(uuid4(), str(uuid4)))  # noqa: WPS125
            product_id = product_data['id']
            created_at = datetime.now()
            project_id = product_data['project_id']

            sqlproduct_data = '{'
            for key, value in product_data.items():
                value = str(value).replace('\\', '/').replace('"', '')
                sqlproduct_data += f'"{key}": "{value}", '
            sqlproduct_data = sqlproduct_data[:-2]
            sqlproduct_data += '}'

            if created:
                sql_create += f""" INSERT INTO changelog_changelog
                (id, created_at, model, record_id, action_on_model, changed_data, project_id)
                VALUES
                ('{id}', '{created_at}', 'product', '{product_id}', 'create', '{sqlproduct_data}', '{project_id}');\r\n
                """
            else:
                sql_create += f""" INSERT INTO changelog_changelog
                (id, created_at, model, record_id, action_on_model, changed_data, project_id)
                VALUES
                ('{id}', '{created_at}', 'product', '{product_id}', 'update', '{sqlproduct_data}', '{project_id}');\r\n
                """

        sql_create += 'COMMIT;\r\n'
        cursor.execute(sql_create)

    def process(self):
        start_time_1 = datetime.now()
        counter = 0
        memory_data_len = len(self.created_data)
        logger.info('Начинаю запись логов создания  ...')
        for chunk in self._chunks(self.created_data, CHUNK_SIZE):
            self._write_chunk(chunk, created=True)
            counter += len(chunk)
            logger.info(
                f'Чанк успешно записан в БД ... ({datetime.now() - start_time_1}) ({counter}/{memory_data_len})',
            )

        start_time_2 = datetime.now()
        counter = 0
        memory_data_len = len(self.updated_data)
        logger.info('Начинаю запись логов обновления  ...')
        for chunk in self._chunks(self.updated_data, CHUNK_SIZE):  # noqa:  WPS440
            self._write_chunk(chunk, created=False)
            counter += len(chunk)
            logger.info(
                f'Чанк успешно записан в БД ... ({datetime.now() - start_time_2}) ({counter}/{memory_data_len})',
            )

        logger.info(f'Логи успешно записаны (всего прошло {datetime.now() - start_time_1}) ...')
