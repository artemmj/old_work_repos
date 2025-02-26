from rest_framework import serializers

from apps.helpers.serializers import PointExtField

from .city import CityArketaCompactReadSerializer, CityArketaSerializer
from .trade_network import TradeNetworkReadSerializer

MIN_LAT, MAX_LAT = -90, 90
MIN_LON, MAX_LON = -180, 180


class TradePointArketaVacantQuerySerializer(serializers.Serializer):
    latitude = serializers.FloatField(help_text='Широта', min_value=MIN_LAT, max_value=MAX_LAT, required=True)
    longitude = serializers.FloatField(help_text='Долгота', min_value=MIN_LON, max_value=MAX_LON, required=True)


class TradePointArketaVacantSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    location = PointExtField()
    max_task_price = serializers.IntegerField()
    address = serializers.CharField()
    network = TradeNetworkReadSerializer()
    city = CityArketaCompactReadSerializer()
    distance = serializers.FloatField(required=False)
    price = serializers.IntegerField()
    full_price = serializers.CharField(required=False)
    time = serializers.FloatField()
    task_count = serializers.IntegerField(required=False)


class TradePointArketaWithoutRegionReadSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    address = serializers.CharField()
    network = TradeNetworkReadSerializer()
    city = CityArketaSerializer()
    location = PointExtField()
    full_address = serializers.CharField(required=False)
