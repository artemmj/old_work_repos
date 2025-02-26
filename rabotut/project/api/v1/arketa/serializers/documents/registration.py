from django.db import models
from rest_framework import serializers


class RegistrationArketaStatusSerializer(models.TextChoices):
    new = 'new', 'new'
    approval = 'approval', 'approval'
    accept = 'accept', 'accept'
    decline = 'decline', 'decline'
    blocked = 'blocked', 'blocked'


class RegistrationArketaReadSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    file = serializers.ListField(child=serializers.UUIDField())  # noqa: WPS110
    status = serializers.ChoiceField(choices=RegistrationArketaStatusSerializer.choices)
    registration_address = serializers.CharField()
    document_status = serializers.ChoiceField(choices=RegistrationArketaStatusSerializer.choices)


class RegistrationArketaWriteSerializer(serializers.Serializer):
    file = serializers.ListField(child=serializers.UUIDField())  # noqa: WPS110
    status = serializers.ChoiceField(choices=RegistrationArketaStatusSerializer.choices, required=False)
    registration_address = serializers.CharField(required=False)
    document_status = serializers.ChoiceField(choices=RegistrationArketaStatusSerializer.choices)
