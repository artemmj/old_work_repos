import json
from io import BytesIO

from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from api.v1.car.serializers.car import (
    BrandSerializer,
    CategorySerializer,
    GenerationSerializer,
    ModelSerializer,
    ModificationSerializer,
)
from apps.car.models.brand import Brand
from apps.car.models.category import Category
from apps.car.models.generation import Generation
from apps.car.models.model import Model
from apps.car.models.modification import Modification
from apps.file.models import DBFile
from apps.helpers.uuid import UUIDEncoder


class Command(BaseCommand):

    def handle(self, **options):    # noqa: WPS110, WPS210
        start_time = now()
        categories = Category.objects.filter(outer_id=1)
        models = Model.objects.filter(category_id=categories.first().id)
        brands = Brand.objects.filter(models__in=models.values_list('pk', flat=True)).distinct()
        generations = Generation.objects.filter(category_id=categories.first().id).exclude(title='')
        modifications = Modification.objects.filter(model__category_id=categories.first().id)

        data_categories = CategorySerializer(categories, many=True).data
        data_brands = BrandSerializer(brands, many=True).data
        data_models = ModelSerializer(models, many=True).data
        data_generations = GenerationSerializer(generations, many=True).data
        data_modifications = ModificationSerializer(modifications, many=True).data

        data = {    # noqa: WPS110
            'categories': data_categories,
            'brands': data_brands,
            'models': data_models,
            'generations': data_generations,
            'modifications': data_modifications,
        }

        json_data = json.dumps(data, cls=UUIDEncoder)
        b = BytesIO()
        b.write(json_data.encode())

        DBFile.objects.create(file=File(b, name='foo.json'))
        end_time = now()
        msg = 'Генерация файла БД завершена за: '
        print(f'{msg}{(end_time - start_time).total_seconds()} сек.', flush=True)   # noqa: T201, WPS421, WPS237
