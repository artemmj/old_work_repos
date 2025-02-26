import csv

from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand, CommandError

from ...models import City


class Command(BaseCommand):
    help = 'Импорт городов из csv справочника'

    def handle(self, *args, **kwargs):  # noqa: WPS110
        try:  # noqa: WPS229
            with open('/app/apps/address/assets/city.csv') as f:
                reader = csv.DictReader(f)
                cities = [
                    City(
                        fias_id=row['fias_id'],
                        title=row['address'],
                        location=Point(float(row['geo_lon']), float(row['geo_lat'])),
                    )
                    for row in reader
                ]
                City.objects.bulk_create(cities)
            print('Импорт городов из csv справочника завершен.')  # noqa: T001 WPS421 T201
        except Exception as e:
            raise CommandError(e)
