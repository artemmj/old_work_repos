import json

from django.utils.timezone import now

from apps.car.models.brand import Brand


def import_brands():
    start_time = now()
    with open('/app/apps/car/assets/vehicle-brands.json', 'r') as brands:
        data_brands = json.load(brands)

    items = [
        Brand(
            outer_id=item['id'],
            title=item['name'],
        )
        for item in data_brands['data']['vehicleBrands']
    ]
    Brand.objects.bulk_update_or_create(items, ['title'], match_field='outer_id')
    end_time = now()

    print(f'Импорт Марок успешно завершен за: {(end_time-start_time).total_seconds()} сек.', flush=True)
