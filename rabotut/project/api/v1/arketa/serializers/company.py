from rest_framework import serializers


class CompanySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    type = serializers.DictField(required=False)
