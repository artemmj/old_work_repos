from django.db import models
from rest_framework import serializers


class DocumentArketaTypeSerializer(models.TextChoices):
    spread = 'spread', 'spread'
    registration = 'registration', 'registration'
    selfie = 'selfie', 'selfie'
    inn = 'inn', 'inn'
    passport = 'passport', 'passport'
    bank_detail = 'bank_detail', 'bank_detail'
    snils = 'snils', 'snils'
    additional = 'additional', 'additional'
    email = 'email', 'email'


class DocumentArketaStatusSerializer(models.TextChoices):
    new = 'new', 'new'
    approval = 'approval', 'approval'
    recognition_succeeded = 'recognition_succeeded', 'recognition_succeeded'
    approved_by_user = 'approved_by_user', 'approved_by_user'
    recognition_failed = 'recognition_failed', 'recognition_failed'
    accept = 'accept', 'accept'
    decline = 'decline', 'decline'
    blocked = 'blocked', 'blocked'


class DocumentAllArketaSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    type = serializers.ChoiceField(choices=DocumentArketaTypeSerializer.choices)
    status = serializers.ChoiceField(choices=DocumentArketaStatusSerializer.choices)
