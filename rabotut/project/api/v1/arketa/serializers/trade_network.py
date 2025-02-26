from rest_framework import serializers

from .file import FileArketaSerializer


class TradeNetworkReadSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    name = serializers.CharField(required=False)
    icon = FileArketaSerializer()
