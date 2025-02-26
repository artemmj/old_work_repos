from rest_framework import serializers

from api.v1.file.serializers import ImageSerializer
from apps.car.models.brand import Brand


class BrandSerializer(serializers.ModelSerializer):
    logo = ImageSerializer()

    class Meta:
        model = Brand
        fields = (
            'id',
            'title',
            'logo',
            'popular',
        )

    select_related_fields = ('logo',)


class BrandShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'title')
