from rest_framework import serializers

from api.v1.tariffs.serializers import TariffReadSerializer
from apps.tariffs.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    tariff = TariffReadSerializer()

    class Meta:
        model = Subscription
        fields = ('id', 'tariff', 'amount', 'is_active', 'auto_renewal', 'start_datetime', 'end_datetime')
