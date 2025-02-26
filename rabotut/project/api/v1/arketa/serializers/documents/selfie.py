from django.db import models
from rest_framework import serializers


class SelfieArketaStatusSerializer(models.TextChoices):
    new = 'new', 'new'
    approval = 'approval', 'approval'
    accept = 'accept', 'accept'
    decline = 'decline', 'decline'
    blocked = 'blocked', 'blocked'


class SelfieArketaReadSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    file = serializers.UUIDField()  # noqa: WPS110
    document_status = serializers.ChoiceField(choices=SelfieArketaStatusSerializer.choices)


class SelfieArketaWriteSerializer(serializers.Serializer):
    file = serializers.UUIDField()  # noqa: WPS110
    document_status = serializers.ChoiceField(choices=SelfieArketaStatusSerializer.choices)
