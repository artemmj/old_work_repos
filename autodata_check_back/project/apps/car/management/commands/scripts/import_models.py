import json

from django.utils.timezone import now

from apps.car.management.commands.scripts.progress import progress
from apps.car.models.brand import Brand
from apps.car.models.category import Category
from apps.car.models.model import Model


def import_models():
    print('Импорт Моделей начался...', flush=True)
    start_time = now()
    with open('/app/apps/car/assets/vehicle-models.json', 'r') as models:
        data_models = json.load(models)

    categories = {item.outer_id: item.id for item in Category.objects.all()}
    brands = {item.outer_id: item.id for item in Brand.objects.all()}

    with Model.objects.bulk_update_or_create_context(
        ['title', 'category_id', 'brand_id', 'year_start', 'year_end'], match_field='outer_id', batch_size=1000
    ) as bulk_kit:
        counter = 0
        len_data = len(data_models['data']['vehicleModels'])
        for item in data_models['data']['vehicleModels']:
            bulk_kit.queue(
                Model(
                    outer_id=item['id'],
                    title=item['name'],
                    category_id=categories.get(item['categoryId']),
                    brand_id=brands.get(item['brandId']),
                    year_start=item['yearFrom'],
                    year_end=item['yearTo'],
                )
            )
            counter += 1
            process_num = counter * 100 / len_data
            progress(process_num)
    end_time = now()

    print(f'Импорт Моделей успешно завершен за: {(end_time-start_time).total_seconds()} сек.', flush=True)
