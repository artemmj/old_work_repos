from rest_framework import serializers

from api.v1.inspection.serializers.services import ValidateInspectionsAttrService
from apps.inspection.models.documents import Documents


class DocumentsReadSerializer(serializers.ModelSerializer):
    answer = serializers.JSONField()

    class Meta:
        model = Documents
        fields = [
            'id',
            'answer',
        ]


class DocumentsWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Documents
        fields = [
            'id',
            'inspection',
            'accreditation_inspection',
            'answer',
        ]

    def validate(self, attrs):
        ValidateInspectionsAttrService(attrs=attrs).process()
        return super().validate(attrs)
