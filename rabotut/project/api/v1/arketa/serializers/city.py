from rest_framework import serializers


class CityArketaCompactReadSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    name = serializers.CharField()


class CityArketaSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    name = serializers.CharField()
    region = serializers.UUIDField()
