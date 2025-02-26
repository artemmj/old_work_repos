from rest_framework import serializers


class MonthStatsRequestSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    date = serializers.DateField(format='%Y-%m-%d')
