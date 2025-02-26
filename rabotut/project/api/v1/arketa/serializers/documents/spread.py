from django.db import models
from rest_framework import serializers


class SpreadArketaStatusSerializer(models.TextChoices):
    new = 'new', 'new'
    approval = 'approval', 'approval'
    accept = 'accept', 'accept'
    decline = 'decline', 'decline'
    blocked = 'blocked', 'blocked'


class SpreadArketaReadSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    gender = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    patronymic = serializers.CharField(required=False)
    fio = serializers.CharField(required=False)
    birth_date = serializers.DateField()
    citizenship = serializers.CharField(required=False)
    number = serializers.CharField()
    series = serializers.CharField()
    department_code = serializers.CharField()
    date_issue = serializers.DateField(required=False)
    issued_by = serializers.CharField(required=False)
    place_of_birth = serializers.CharField(required=False)
    document_status = serializers.ChoiceField(choices=SpreadArketaStatusSerializer.choices)


class SpreadArketaWriteSerializer(serializers.Serializer):
    gender = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    patronymic = serializers.CharField(required=False)
    fio = serializers.CharField(required=False)
    birth_date = serializers.DateField()
    citizenship = serializers.CharField(required=False)
    number = serializers.CharField()
    series = serializers.CharField()
    department_code = serializers.CharField()
    date_issue = serializers.DateField(required=False)
    issued_by = serializers.CharField(required=False)
    place_of_birth = serializers.CharField(required=False)
    document_status = serializers.ChoiceField(choices=SpreadArketaStatusSerializer.choices)
