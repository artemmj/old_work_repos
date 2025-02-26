from rest_framework import serializers

from api.v1.inspection.serializers.services import ValidateInspectionsAttrService
from apps.helpers.serializers import EagerLoadingSerializerMixin
from apps.inspection.models.inspection import Inspection
from apps.inspection.models.photos import Photos


class PhotosReadSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    answer = serializers.JSONField()

    class Meta:
        model = Photos
        fields = [
            'id',
            'answer',
        ]


class PhotosWriteSerializer(serializers.ModelSerializer):
    inspection = serializers.PrimaryKeyRelatedField(queryset=Inspection.objects.all(), required=False)

    class Meta:
        model = Photos
        fields = [
            'id',
            'answer',
            'inspection',
            'accreditation_inspection',
        ]

    def validate(self, attrs):
        ValidateInspectionsAttrService(attrs=attrs).process()
        return super().validate(attrs)
