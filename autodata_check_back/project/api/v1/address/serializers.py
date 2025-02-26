from constance import config
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.city.serializers import CityReadSerializer
from apps.address.models import Address, City
from apps.helpers.serializers import PointExtField
from apps.inspection.models.inspection import Inspection


class AddressDadataQuerySerializer(serializers.Serializer):
    query = serializers.CharField(required=False)
    lat = serializers.FloatField(required=False)
    lon = serializers.FloatField(required=False)

    def validate(self, attrs):
        if attrs.get('query') and (attrs.get('lat') and attrs.get('lon')):  # noqa:  WPS221
            raise ValidationError({'error': config.ADDRESS_QUERY_AND_LOCATION_TOGETHER_ERROR})
        return attrs


class AddressDadataResultSerializer(serializers.Serializer):
    value = serializers.CharField()   # noqa: WPS110
    unrestricted_value = serializers.CharField()
    longitude = serializers.CharField()
    latitude = serializers.CharField()
    city_fias_id = serializers.CharField()


class AddressReadSerializer(serializers.ModelSerializer):
    city = CityReadSerializer()
    street = serializers.SerializerMethodField(read_only=True)
    location = PointExtField()

    class Meta:
        model = Address
        fields = ('id', 'city', 'title', 'street', 'location', 'inspections')

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_street(self, instance):
        if instance.city:
            return instance.title.replace(instance.city.title, '')[2:]
        return None


class AddressWriteSerializer(serializers.ModelSerializer):
    location = PointExtField()
    inspection = serializers.PrimaryKeyRelatedField(queryset=Inspection.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Address
        fields = ('id', 'city', 'title', 'location', 'inspection')

    def create(self, validated_data):
        inspection = validated_data.pop('inspection', None)
        instance = super().create(validated_data)
        if inspection:
            inspection.address = instance
            inspection.save()
        return instance
