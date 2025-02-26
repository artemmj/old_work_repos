from rest_framework import serializers

from api.v1.inspection.serializers.services import ValidateInspectionsAttrService
from apps.inspection.models.inspection import Inspection
from apps.inspection.models.paintwork import Paintwork


class PaintworkReadSerializer(serializers.ModelSerializer):
    answer = serializers.JSONField()

    class Meta:
        model = Paintwork
        fields = [
            'id',
            'answer',
        ]


class PaintworkWriteSerializer(serializers.ModelSerializer):
    inspection = serializers.PrimaryKeyRelatedField(queryset=Inspection.objects.all(), required=False)

    class Meta:
        model = Paintwork
        fields = [
            'id',
            'answer',
            'inspection',
            'accreditation_inspection',
        ]

    def validate(self, attrs):
        ValidateInspectionsAttrService(attrs=attrs).process()
        return super().validate(attrs)
