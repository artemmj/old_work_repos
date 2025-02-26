from rest_framework import serializers

from api.v1.inspection.serializers.services import ValidateInspectionsAttrService
from apps.inspection.models.client import Client
from apps.inspection.models.inspection import Inspection


class ClientReadSerializer(serializers.ModelSerializer):
    answer = serializers.JSONField()

    class Meta:
        model = Client
        fields = [
            'id',
            'answer',
        ]


class ClientWriteSerializer(serializers.ModelSerializer):
    inspection = serializers.PrimaryKeyRelatedField(queryset=Inspection.objects.all(), required=False)

    class Meta:
        model = Client
        fields = [
            'id',
            'inspection',
            'accreditation_inspection',
            'answer',
        ]

    def validate(self, attrs):
        ValidateInspectionsAttrService(attrs=attrs).process()
        return super().validate(attrs)
