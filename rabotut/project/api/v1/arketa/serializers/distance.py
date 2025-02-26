from rest_framework import serializers


class DistanceQueryParamSerializer(serializers.Serializer):
    latitude = serializers.FloatField(
        help_text='Широта',
        min_value=-90,  # noqa: WPS432
        max_value=90,  # noqa: WPS432
        required=True,
    )
    longitude = serializers.FloatField(
        help_text='Долгота',
        min_value=-180,  # noqa: WPS432
        max_value=180,  # noqa: WPS432
        required=True,
    )


class DistanceTradePointQueryParamsSerializer(DistanceQueryParamSerializer):
    trade_point = serializers.ListField(child=serializers.UUIDField(), required=False)
    limit = serializers.IntegerField(required=False)
