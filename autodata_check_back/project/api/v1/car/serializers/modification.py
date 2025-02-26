from rest_framework import serializers

from api.v1.car.serializers.brand import BrandSerializer
from api.v1.car.serializers.generation import GenerationReadSerializer
from api.v1.car.serializers.model import ModelReadSerializer
from apps.car.models import BodyTypeChoices, DriveTypeChoices, EngineTypeChoices, GearboxTypeChoices
from apps.car.models.modification import Modification
from apps.helpers.serializers import EagerLoadingSerializerMixin, EnumField


class ModificationSerializer(serializers.ModelSerializer):
    body_type = EnumField(enum_class=BodyTypeChoices)
    gearbox_type = EnumField(enum_class=GearboxTypeChoices)
    drive_type = EnumField(enum_class=DriveTypeChoices)
    engine_type = EnumField(enum_class=EngineTypeChoices)

    class Meta:
        model = Modification
        fields = (
            'id',
            'title',
            'brand',
            'model',
            'generation',
            'year_start',
            'year_end',
            'drive_type',
            'engine_type',
            'gearbox_type',
            'body_type',
            'engine_volume',
            'engine_power',
        )


class ModificationReadSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    body_type = EnumField(enum_class=BodyTypeChoices)
    gearbox_type = EnumField(enum_class=GearboxTypeChoices)
    drive_type = EnumField(enum_class=DriveTypeChoices)
    engine_type = EnumField(enum_class=EngineTypeChoices)
    model = ModelReadSerializer()
    brand = BrandSerializer()
    generation = GenerationReadSerializer()

    select_related_fields = ('brand', 'model', 'generation')

    class Meta:
        model = Modification
        fields = (
            'id',
            'title',
            'year_start',
            'year_end',
            'drive_type',
            'engine_type',
            'gearbox_type',
            'body_type',
            'brand',
            'model',
            'generation',
        )


class CarTypeEnumSerializer(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.CharField()
