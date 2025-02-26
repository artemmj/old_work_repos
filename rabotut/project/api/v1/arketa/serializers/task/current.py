from django.db import models
from rest_framework import serializers

MIN_LONG = -90
MAX_LONG = 90
MIN_LAT = -180
MAX_LAT = 180


class TaskArketaCurrentStatusesChoices(models.TextChoices):
    today = 'today', 'today'
    future = 'future', 'future'
    ready = 'ready', 'ready'
    overdue = 'overdue', 'overdue'


class TaskArketaCurrentOrderingChoices(models.TextChoices):
    status = 'status', 'status'
    _status = '-status', '-status'
    execution_at = 'execution_at', 'execution_at'
    _execution_at = '-execution_at', '-execution_at'
    completion_date = 'completion_date', 'completion_date'
    _completion_date = '-completion_date', '-completion_date'


class TaskArketaCurrentQuerySerializer(serializers.Serializer):
    latitude = serializers.FloatField(help_text='Широта', min_value=MIN_LONG, max_value=MAX_LONG, required=False)
    longitude = serializers.FloatField(help_text='Долгота', min_value=MIN_LAT, max_value=MAX_LAT, required=False)
    status = serializers.ChoiceField(choices=TaskArketaCurrentStatusesChoices.choices, required=False)
    ordering = serializers.ChoiceField(choices=TaskArketaCurrentOrderingChoices.choices, required=False)
