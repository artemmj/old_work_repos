from rest_framework import serializers

from apps.helpers.serializers import EnumField
from apps.tariffs.models import Tariff, TariffPeriodChoices


class TariffReadSerializer(serializers.ModelSerializer):
    period = EnumField(enum_class=TariffPeriodChoices)

    class Meta:
        model = Tariff
        fields = ('id', 'title', 'subtitle', 'description', 'period', 'amount')


class TariffWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = ('id', 'title', 'subtitle', 'description', 'period', 'amount', 'organization')
        read_only_fields = ('id',)
