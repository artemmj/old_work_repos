from typing import Dict, List

from dadata import Dadata
from django.conf import settings

from apps.helpers.services import AbstractService


class DadataSearchAddressService(AbstractService):
    """Сервис по поиску адресов в Dadata."""

    def transform_response(self, response: List[Dict]) -> List[Dict]:
        return [
            {
                'value': r['value'],
                'unrestricted_value': r['unrestricted_value'],
                'longitude': r['data']['geo_lon'],
                'latitude': r['data']['geo_lat'],
                'city_fias_id': r['data']['city_fias_id'],
            }
            for r in response
        ]

    def process(self, query=None, lat=None, lon=None) -> List[Dict]:
        with Dadata(settings.DADATA_TOKEN, settings.DADATA_SECRET) as dadata:
            if query:
                response = dadata.suggest(name='address', query=query)
            else:
                response = dadata.geolocate(name='address', lat=lat, lon=lon, radius_meters=1)
        return self.transform_response(response)


class DadataFindByINNService(AbstractService):
    """Сервис по поиску организаций по инн в Dadata."""

    def process(self, inn: str):
        with Dadata(settings.DADATA_TOKEN, settings.DADATA_SECRET) as dadata:
            response = dadata.find_by_id(name='party', query=inn)
            return response  # noqa: WPS331
