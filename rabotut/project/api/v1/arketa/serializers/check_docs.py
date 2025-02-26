from rest_framework import serializers

from apps.helpers.serializers import EnumSerializer


class CheckDocResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    type = EnumSerializer(required=True)
    status = EnumSerializer(required=True)
