from rest_framework import serializers

from api.v1.car.serializers.brand import BrandSerializer
from api.v1.car.serializers.category import CategorySerializer
from api.v1.car.serializers.model import ModelReadSerializer
from apps.car.models.generation import Generation
from apps.helpers.serializers import EagerLoadingSerializerMixin


class GenerationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Generation
        fields = (
            'id',
            'title',
            'brand',
            'model',
            'year_start',
            'year_end',
        )


class GenerationReadSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    model = ModelReadSerializer()
    brand = BrandSerializer()
    category = CategorySerializer()

    select_related_fields = ('category', 'brand', 'model')

    class Meta:
        model = Generation
        fields = (
            'id',
            'title',
            'category',
            'brand',
            'model',
            'year_start',
            'year_end',
        )
