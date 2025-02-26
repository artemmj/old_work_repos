import urllib
from typing import Dict

from .api_client import ArketaApiClient


class ArketaTradepointApiClient(ArketaApiClient):
    def trade_point_vacant(self, serializer_data: Dict):
        """Cписок торговых точек."""
        query_params = {
            'distance__latitude': serializer_data.get('latitude'),
            'distance__longitude': serializer_data.get('longitude'),
            'limit': 50,
        }
        url = f'{self.api_url}trade_point/vacant/?{urllib.parse.urlencode(query_params)}'
        return self._request('get', url)
