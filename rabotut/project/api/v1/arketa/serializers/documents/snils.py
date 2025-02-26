from django.db import models
from rest_framework import serializers


class SnilsArketaStatusSerializer(models.TextChoices):
    new = 'new', 'new'
    approval = 'approval', 'approval'
    accept = 'accept', 'accept'
    decline = 'decline', 'decline'
    blocked = 'blocked', 'blocked'


class SnilsArketaReadSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    value = serializers.CharField()  # noqa: WPS110
    document_status = serializers.ChoiceField(choices=SnilsArketaStatusSerializer.choices)


class SnilsArketaWriteSerializer(serializers.Serializer):
    value = serializers.CharField()  # noqa: WPS110
    document_status = serializers.ChoiceField(choices=SnilsArketaStatusSerializer.choices)
