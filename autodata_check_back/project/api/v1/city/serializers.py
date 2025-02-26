from constance import config
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.address.models import City
from apps.helpers.serializers import PointExtField


class CityReadSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='fias_id')
    location = PointExtField()

    class Meta:
        model = City
        fields = ('id', 'title', 'location', 'inspection_price')


class CityWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('title', 'inspection_price')


class ImportExcelRequestSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)

    def validate_file(self, field):
        file_ext = field.name[-5:]
        if file_ext != '.xlsx':
            raise ValidationError({'file': config.CITY_IMPORT_NEED_XLSX_ERROR})
        return field
