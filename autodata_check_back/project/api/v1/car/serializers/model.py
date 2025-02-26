from rest_framework import serializers

from api.v1.car.serializers.brand import BrandSerializer
from api.v1.car.serializers.category import CategorySerializer
from apps.car.models.model import Model
from apps.helpers.serializers import EagerLoadingSerializerMixin


class ModelSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    select_related_fields = ('brand', 'category')

    class Meta:
        model = Model
        fields = (
            'id',
            'title',
            'brand',
            'category',
            'year_start',
            'year_end',
            'popular',
        )


class ModelReadSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer()

    select_related_fields = ('brand', 'category')

    class Meta:
        model = Model
        fields = (
            'id',
            'title',
            'brand',
            'category',
        )


class ModelCompactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ('id', 'title')


class ModelYearsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ('year_start', 'year_end')
