import re

from constance import config
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.car.serializers.brand import BrandSerializer, BrandShortSerializer
from api.v1.car.serializers.category import CategorySerializer
from api.v1.car.serializers.generation import GenerationSerializer
from api.v1.car.serializers.model import ModelCompactSerializer, ModelSerializer
from api.v1.car.serializers.modification import ModificationSerializer
from api.v1.inspection.serializers.services import ValidateInspectionsAttrService
from apps.car.models import BodyTypeChoices, DriveTypeChoices, EngineTypeChoices, GearboxTypeChoices
from apps.car.models.car import Car
from apps.helpers.serializers import EagerLoadingSerializerMixin, EnumField


class CarCompactSerializer(serializers.ModelSerializer):
    brand = BrandShortSerializer()
    model = ModelCompactSerializer()

    class Meta:
        model = Car
        fields = ('id', 'brand', 'model', 'gov_number', 'vin_code', 'production_year')


class CarReadSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()
    model = ModelSerializer()
    generation = GenerationSerializer()
    modification = ModificationSerializer()
    body_type = EnumField(enum_class=BodyTypeChoices)
    gearbox_type = EnumField(enum_class=GearboxTypeChoices)
    drive_type = EnumField(enum_class=DriveTypeChoices)
    engine_type = EnumField(enum_class=EngineTypeChoices)

    select_related_fields = ('category', 'brand', 'model', 'generation', 'modification')

    class Meta:
        model = Car
        fields = (
            'id',
            'vin_code',
            'unstandart_vin',
            'gov_number',
            'category',
            'brand',
            'model',
            'generation',
            'modification',
            'body_type',
            'gearbox_type',
            'drive_type',
            'engine_type',
            'color',
            'mileage',
            'mileage_unknown',
            'engine_volume',
            'engine_power',
            'production_year',
            'inspection',
            'accreditation_inspection',
        )


class CarWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = (
            'id',
            'vin_code',
            'unstandart_vin',
            'gov_number',
            'category',
            'brand',
            'model',
            'generation',
            'modification',
            'body_type',
            'gearbox_type',
            'drive_type',
            'engine_type',
            'color',
            'mileage',
            'mileage_unknown',
            'engine_volume',
            'engine_power',
            'production_year',
            'inspection',
            'accreditation_inspection',
        )

    def validate(self, attrs):
        ValidateInspectionsAttrService(attrs=attrs).process()
        return super().validate(attrs)

    def validate_gov_number(self, attr):
        # Форматы кириллицей 'А777АА77', 'А777АА777', 'АА777А77',
        # 'АА777 77', 'АА777 777', 'АА7777 77', 'АА7777 777'
        cyrillic_pattern = r'^[А-Я\-\s]{1,2}[0-9]{3}(?<!0{3})[А-Я\-\s]{1,2}[0-9]{2,3}$'

        # Форматы латиницей '7777 AA-7', '777 AAA 77'
        latin_pattern = r'^[0-9]{3,4}(?<!0{3})\s[A-Z\-\s]{2,4}[0-9]{1,2}(?<!0{3})'

        # форматы для смешанных номеров
        # 'АА7777 77'
        # 'АА7777 777'
        # 'A 777 AA 77'
        # 'A 777 AA 777'
        # 'AA 777 A 77'
        # 'AA 777 77'
        # 'АА 7777 77'

        combine_pattern = r'^[A-Z,А-Я\-\s]{1,3}[\d\s]{4}(?<!0{3})[A-Z,А-Я\-\s]{1,2}[\d\s]{2,4}$'

        if (attr  # noqa: WPS337
            and re.fullmatch(cyrillic_pattern, attr) is None  # noqa: WPS337
            and re.fullmatch(latin_pattern, attr) is None  # noqa: WPS221, WPS337
            and re.fullmatch(combine_pattern, attr) is None
        ):   # noqa: E124
            raise ValidationError(config.CAR_INVALID_GOV_NUM_ERROR)
        return attr
