import json

from django.utils.timezone import now

from apps.car.management.commands.scripts.progress import progress
from apps.car.models.brand import Brand
from apps.car.models.generation import Generation
from apps.car.models.model import Model
from apps.car.models.modification import (
    BodyTypeChoices,
    DriveTypeChoices,
    EngineTypeChoices,
    GearboxTypeChoices,
    Modification,
)


def import_modifications():
    print('Импорт Модификаций начался...', flush=True)
    start_time = now()
    with open('/app/apps/car/assets/vehicle-modifications.json', 'r') as modifications:
        data_modifications = json.load(modifications)

    brands = {item.outer_id: item.id for item in Brand.objects.all()}
    models = {item.outer_id: item.id for item in Model.objects.all()}
    generations = {item.outer_id: item.id for item in Generation.objects.all()}

    with Modification.objects.bulk_update_or_create_context(
        [
            'title', 'brand_id', 'model_id',
            'generation_id', 'year_start', 'year_end',
            'body_type', 'gearbox_type', 'drive_type',
            'engine_type', 'engine_volume', 'engine_power',
        ],
        match_field='outer_id',
        batch_size=1000,
    ) as bulk_kit:
        counter = 0
        len_data = len(data_modifications['data']['vehicleModifications'])
        for item in data_modifications['data']['vehicleModifications']:
            bulk_kit.queue(
                Modification(
                    outer_id=item['id'],
                    title=item['name'],
                    brand_id=brands.get(item['brandId']),
                    model_id=models.get(item['modelId']),
                    generation_id=generations.get(item['generationId']),
                    year_start=item['yearFrom'],
                    year_end=item['yearTo'],
                    body_type=item['bodyType'] if item['bodyType'] in BodyTypeChoices.values else None,
                    gearbox_type=item['gearboxType'] if item['gearboxType'] in GearboxTypeChoices.values else None,
                    drive_type=item['driveType'] if item['driveType'] in DriveTypeChoices.values else None,
                    engine_type=item['engineType'] if item['engineType'] in EngineTypeChoices.values else None,
                    engine_volume=item['engineVolume'],
                    engine_power=item['enginePower'],
                )
            )
            counter += 1
            process_num = counter * 100 / len_data
            progress(process_num)
    end_time = now()

    print(f'Импорт Модификаций успешно завершен за: {(end_time-start_time).total_seconds()} сек.', flush=True)
