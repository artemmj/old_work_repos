from rest_framework import serializers

from api.v1.inspection.serializers.services import ValidateInspectionsAttrService
from apps.inspection.models.equipment import Equipment
from apps.inspection.models.inspection import Inspection


class EquipmentReadSerializer(serializers.ModelSerializer):
    answer = serializers.JSONField()

    class Meta:
        model = Equipment
        fields = [
            'id',
            'answer',
        ]


class EquipmentWriteSerializer(serializers.ModelSerializer):
    inspection = serializers.PrimaryKeyRelatedField(queryset=Inspection.objects.all(), required=False)

    class Meta:
        model = Equipment
        fields = [
            'id',
            'inspection',
            'accreditation_inspection',
            'answer',
        ]

    def validate(self, attrs):
        ValidateInspectionsAttrService(attrs=attrs).process()
        return super().validate(attrs)
