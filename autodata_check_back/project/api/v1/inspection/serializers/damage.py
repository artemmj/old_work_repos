from rest_framework import serializers

from api.v1.inspection.serializers.services import ValidateInspectionsAttrService
from apps.helpers.serializers import EagerLoadingSerializerMixin
from apps.inspection.models.damage import Damage
from apps.inspection.models.inspection import Inspection


class DamageReadSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    answer = serializers.JSONField()

    class Meta:
        model = Damage
        fields = [
            'id',
            'answer',
        ]


class DamageWriteSerializer(serializers.ModelSerializer):
    inspection = serializers.PrimaryKeyRelatedField(
        queryset=Inspection.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Damage
        fields = [
            'id',
            'inspection',
            'accreditation_inspection',
            'answer',
        ]

    def validate(self, attrs):
        ValidateInspectionsAttrService(attrs=attrs).process()
        return super().validate(attrs)
