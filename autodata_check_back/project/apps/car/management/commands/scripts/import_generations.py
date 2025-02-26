import json

from django.utils.timezone import now

from apps.car.management.commands.scripts.progress import progress
from apps.car.models.brand import Brand
from apps.car.models.category import Category
from apps.car.models.generation import Generation
from apps.car.models.model import Model


def import_generations():
    print('Импорт Поколений начался...', flush=True)
    start_time = now()
    with open('/app/apps/car/assets/vehicle-generations.json', 'r') as generations:
        data_generations = json.load(generations)

    categories = {item.outer_id: item.id for item in Category.objects.all()}
    brands = {item.outer_id: item.id for item in Brand.objects.all()}
    models = {item.outer_id: item.id for item in Model.objects.all()}

    with Generation.objects.bulk_update_or_create_context(
        ['title', 'brand_id', 'category_id', 'model_id', 'year_start', 'year_end'],
        match_field='outer_id',
        batch_size=1000,
    ) as bulk_kit:
        counter = 0
        len_data = len(data_generations['data']['vehicleGenerations'])
        for item in data_generations['data']['vehicleGenerations']:
            bulk_kit.queue(
                Generation(
                    outer_id=item['id'],
                    title=item['name'] if item['name'] else f'{item["yearFrom"]}-{item["yearTo"]}',
                    category_id=categories.get(item['categoryId']),
                    brand_id=brands.get(item['brandId']),
                    model_id=models.get(item['modelId']),
                    year_start=item['yearFrom'],
                    year_end=item['yearTo'],
                )
            )
            counter += 1
            process_num = counter * 100 / len_data
            progress(process_num)
    end_time = now()

    print(f'Импорт Поколений успешно завершен за: {(end_time-start_time).total_seconds()} сек.', flush=True)
