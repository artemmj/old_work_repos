from rest_framework import serializers

from api.v1.inspection.serializers.services import ValidateInspectionsAttrService
from apps.helpers.serializers import EagerLoadingSerializerMixin
from apps.inspection.models.inspection import Inspection
from apps.inspection.models.lift import Lift


class LiftReadSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    answer = serializers.JSONField()

    class Meta:
        model = Lift
        fields = [
            'id',
            'answer',
        ]


class LiftWriteSerializer(serializers.ModelSerializer):
    inspection = serializers.PrimaryKeyRelatedField(queryset=Inspection.objects.all(), required=False)

    class Meta:
        model = Lift
        fields = [
            'id',
            'inspection',
            'accreditation_inspection',
            'answer',
        ]

    def validate(self, attrs):
        ValidateInspectionsAttrService(attrs=attrs).process()
        return super().validate(attrs)
