from django.utils.timezone import now

from apps.car.models import Modification
from apps.car.models.car import Car


def modifications():
    for mod in Modification.objects.values(
        'title', 'brand', 'model', 'generation', 'year_start', 'year_end', 'body_type',
        'gearbox_type', 'drive_type', 'engine_type', 'engine_volume', 'engine_power',
    ).distinct():
        yield mod


def delete_duplicates_modifications():
    print('Удаление дубликатов модификаций началось...', flush=True)
    start_time = now()
    for_delete_ids = []
    for mod in modifications():
        item = Modification.objects.filter(**mod)
        if item.count() > 1:
            first = item.first()
            items = item.exclude(id=first.id)
            for_delete_ids.append(items.values_list('id', flat=True))
    for_delete_ids = [i[0] for i in for_delete_ids]
    res = Modification.objects.filter(id__in=for_delete_ids)
    Car.objects.filter(modification__in=res).delete()
    res.delete()
    end_time = now()

    print(f'Удаление дубликатов модификаций завершено за: {(end_time - start_time).total_seconds()} сек.', flush=True)
