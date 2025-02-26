import json

from django.utils.timezone import now

from apps.car.models.category import Category


def import_categories():
    start_time = now()
    with open('/app/apps/car/assets/vehicle-categories.json', 'r') as categories:
        data_categories = json.load(categories)

    items = [
        Category(
            outer_id=item['id'],
            title=item['name'],
        )
        for item in data_categories['data']['vehicleCategories']
    ]
    Category.objects.bulk_update_or_create(items, ['title'], match_field='outer_id')
    end_time = now()

    print(f'Импорт Типов ТС успешно завершен за: {(end_time-start_time).total_seconds()} сек.', flush=True)
