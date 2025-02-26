from django.db import models
from rest_framework import serializers

from .file import TaskFileSerializer


class RecognitionSKUAnswerStatus(models.TextChoices):
    in_stock = 'in_stock', 'in_stock'
    recognition_error = 'recognition_error', 'recognition_error'
    out_of_stock = 'out_of_stock', 'out_of_stock'


class RecognitionSKUAnswerSerializer(serializers.Serializer):
    sku_id = serializers.UUIDField()
    reason_id = serializers.UUIDField()
    count = serializers.IntegerField()
    status = serializers.ChoiceField(choices=RecognitionSKUAnswerStatus.choices)
    confirmation_photo = TaskFileSerializer(required=False)


class RecognitionAnswerSerializer(serializers.Serializer):
    skues = RecognitionSKUAnswerSerializer(many=True, required=False)


class TaskFileScannerSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    type = serializers.CharField()


class ScannerAnswerSerializer(serializers.Serializer):
    is_barcode_recognized = serializers.BooleanField()
    is_barcode_matched = serializers.BooleanField()
    is_goods_wrong = serializers.BooleanField()
    barcode = serializers.CharField()
    price = serializers.FloatField()
    promotion_price = serializers.FloatField()
    card_price = serializers.FloatField()
    photos = TaskFileScannerSerializer(many=True)


class TaskTypeChoices(models.TextChoices):
    numeric = 'numeric', 'numeric'
    boolean = 'boolean', 'boolean'
    textual = 'textual', 'textual'
    photo = 'photo', 'photo'
    choice = 'choice', 'choice'
    multi_choice = 'multi_choice', 'multi_choice'
    monetary = 'monetary', 'monetary'
    date = 'date', 'date'
    recognition = 'recognition', 'recognition'
    scanner = 'scanner', 'scanner'


class TaskAnswerSerializer(serializers.Serializer):  # noqa: WPS214
    numeric = serializers.FloatField(required=False)
    monetary = serializers.FloatField(required=False)
    boolean = serializers.BooleanField(required=False)
    textual = serializers.CharField(required=False)
    photo = TaskFileSerializer(many=True, required=False)
    date = serializers.DateField(required=False)
    choice = serializers.CharField(required=False)
    multi_choice = serializers.ListField(child=serializers.CharField(), required=False)
    recognition = RecognitionAnswerSerializer(required=False)
    scanner = ScannerAnswerSerializer(many=True, required=False)
    id = serializers.UUIDField()
    type = serializers.ChoiceField(choices=TaskTypeChoices.choices)
