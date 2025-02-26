from drf_yasg import openapi
from rest_framework import serializers

from api.v1.product.serializers import ScannedProductSerializer
from apps.helpers.serializers import EnumField
from apps.task.models import Task, TaskStatusChoices, TaskTypeChoices
from apps.zone.models import Zone, ZoneStatusChoices


class TaskZoneReadSerializer(serializers.ModelSerializer):
    status = EnumField(enum_class=ZoneStatusChoices)

    class Meta:
        model = Zone
        fields = ('id', 'serial_number', 'title', 'storage_name', 'code', 'status')


class TaskReadSerializer(serializers.ModelSerializer):
    zone = TaskZoneReadSerializer()
    type = EnumField(enum_class=TaskTypeChoices)
    status = EnumField(enum_class=TaskStatusChoices)
    scanned_products = ScannedProductSerializer(many=True)

    class Meta:
        model = Task
        fields = ('id', 'terminal', 'zone', 'type', 'status', 'result', 'scanned_products')
        swagger_schema_fields = {
            'type': openapi.TYPE_OBJECT,
            'title': 'TaskRead',
        }
