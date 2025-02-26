from django.db import models
from rest_framework import serializers


class InnArketaStatusSerializer(models.TextChoices):
    new = 'new', 'new'
    approval = 'approval', 'approval'
    accept = 'accept', 'accept'
    decline = 'decline', 'decline'
    blocked = 'blocked', 'blocked'


class InnArketaReadSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    value = serializers.CharField()  # noqa: WPS110
    document_status = serializers.ChoiceField(choices=InnArketaStatusSerializer.choices)


class InnArketaWriteSerializer(serializers.Serializer):
    value = serializers.CharField()  # noqa: WPS110
    document_status = serializers.ChoiceField(choices=InnArketaStatusSerializer.choices)
