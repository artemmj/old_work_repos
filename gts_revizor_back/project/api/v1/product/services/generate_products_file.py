import json
import logging
import os
from datetime import datetime
from secrets import token_urlsafe

from django.conf import settings

from api.v1.product import serializers as product_serializers
from apps import app
from apps.helpers.services import AbstractService
from apps.product.models import FileOfProjectProducts, Product
from apps.project.models import Project

logger = logging.getLogger('django')


@app.task
def generate_products_file_celery_wrapper(project_id: str):
    return GenerateProductsFileService(project_id).process()


class GenerateProductsFileService(AbstractService):
    def __init__(self, project_id: str):
        self.project = Project.objects.get(pk=project_id)
        try:
            self.file_of_products = FileOfProjectProducts.objects.get(project=self.project)
        except FileOfProjectProducts.DoesNotExist:
            self.file_of_products = None

    def process(self):
        logger.info('Начинаю запись файла с товарами ...')
        start_time = datetime.now()
        if self.file_of_products:
            path = self.file_of_products.products_file
            self.file_of_products.delete()
            try:
                os.remove(path)
            except FileNotFoundError:
                pass  # noqa: WPS420

        products = Product.objects.filter(project=self.project)
        serialized_data = product_serializers.ProductReadSerializer(products, many=True).data

        filename = f'{token_urlsafe(8)}.txt'
        path_prefx = f'{settings.MEDIA_ROOT}/products_upload'
        if not os.path.exists(path_prefx):
            os.makedirs(path_prefx)
        file_dest = f'{path_prefx}/{filename}'

        with open(file_dest, 'w', encoding='windows-1251') as outfile:
            json.dump(serialized_data, outfile)

        FileOfProjectProducts.objects.create(
            project=self.project,
            products_file=file_dest,
        )

        logger.info(f'Файл с товарами успено записан и сохранен ... ({datetime.now() - start_time})')

        return file_dest
