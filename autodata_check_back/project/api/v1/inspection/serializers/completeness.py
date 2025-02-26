from rest_framework import serializers

from api.v1.inspection.serializers.services import ValidateInspectionsAttrService
from apps.inspection.models.completeness import Completeness
from apps.inspection.models.inspection import Inspection


class CompletenessReadSerializer(serializers.ModelSerializer):
    answer = serializers.JSONField()

    class Meta:
        model = Completeness
        fields = [
            'id',
            'answer',
        ]


class CompletenessWriteSerializer(serializers.ModelSerializer):
    inspection = serializers.PrimaryKeyRelatedField(queryset=Inspection.objects.all(), required=False)

    class Meta:
        model = Completeness
        fields = [
            'id',
            'inspection',
            'accreditation_inspection',
            'answer',
        ]

    def validate(self, attrs):
        ValidateInspectionsAttrService(attrs=attrs).process()
        return super().validate(attrs)
