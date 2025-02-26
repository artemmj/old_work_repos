from rest_framework import serializers


class BrandSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
