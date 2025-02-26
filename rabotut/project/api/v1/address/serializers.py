from rest_framework import serializers

from apps.address.models import City
from apps.helpers.serializers import PointExtField


class CitySerializer(serializers.ModelSerializer):
    location = PointExtField()

    class Meta:
        model = City
        fields = ('id', 'name', 'location')
