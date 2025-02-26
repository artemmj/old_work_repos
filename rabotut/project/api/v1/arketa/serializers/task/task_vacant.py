from rest_framework import serializers

from ..company import CompanySerializer
from ..file import FileArketaExtendedSerializer
from ..order_frequency_types import OrderFrequencyTypes
from ..sku import SKUReadSerializer

MIN_LAT, MAX_LAT = -90, 90
MIN_LON, MAX_LON = -180, 180


class TaskArketaVacantQuerySerializer(serializers.Serializer):
    latitude = serializers.FloatField(help_text='Широта', min_value=MIN_LAT, max_value=MAX_LAT, required=True)
    longitude = serializers.FloatField(help_text='Долгота', min_value=MIN_LON, max_value=MAX_LON, required=True)
    trade_point = serializers.ListField(child=serializers.UUIDField(), required=False)
    is_liked = serializers.BooleanField(required=False)
    limit = serializers.IntegerField(required=False)


class TaskArketaVacantSerializer(serializers.Serializer):  # noqa: WPS214
    id = serializers.UUIDField(required=False)
    name = serializers.CharField()
    description = serializers.CharField()
    cost = serializers.FloatField()
    time = serializers.IntegerField()
    time = serializers.FloatField()
    price = serializers.IntegerField()
    full_price = serializers.IntegerField(required=False)
    completion_date = serializers.DateField()
    company = CompanySerializer()
    comment = serializers.CharField()
    additional_files = FileArketaExtendedSerializer(many=True)
    planogram = FileArketaExtendedSerializer()
    planograms = FileArketaExtendedSerializer(many=True)
    need_execution = serializers.BooleanField(required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    days = serializers.ListSerializer(child=serializers.DateField())
    frequency = serializers.ChoiceField(choices=OrderFrequencyTypes.choices)
    skues = SKUReadSerializer(many=True, required=False)
    work_kind = serializers.CharField()
    trade_point_id = serializers.UUIDField()
    is_liked = serializers.BooleanField(required=True)
    viewing = serializers.IntegerField()
