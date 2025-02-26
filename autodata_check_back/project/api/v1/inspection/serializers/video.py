from rest_framework import serializers

from api.v1.inspection.serializers.services import ValidateInspectionsAttrService
from apps.helpers.serializers import EagerLoadingSerializerMixin
from apps.inspection.models.video import Video


class VideoReadSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    answer = serializers.JSONField()

    class Meta:
        model = Video
        fields = ('id', 'created_at', 'answer')
        read_only_fields = ('id', 'created_at')


class VideoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'inspection', 'answer', 'accreditation_inspection')
        read_only_fields = ('id', 'created_at')

    def validate(self, attrs):
        ValidateInspectionsAttrService(attrs=attrs).process()
        return super().validate(attrs)
