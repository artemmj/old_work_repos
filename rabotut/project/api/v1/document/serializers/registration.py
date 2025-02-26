from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.v1.file.serializers import FileSerializer
from apps.document.helpers import AdminOrCurrentUserDefault
from apps.document.models import Registration
from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.document.services import ApprovalDocumentService, GetOrCreateDocumentService
from apps.document.services.calculate_user_status import CalculateUserStatusService
from apps.helpers.serializers import EnumField

User = get_user_model()


class RegistrationReadSerializer(serializers.ModelSerializer):
    file = FileSerializer(many=True)  # noqa: WPS110
    status = EnumField(enum_class=BaseUserDocumentStatuses)

    class Meta:
        model = Registration
        fields = (
            'id',
            'created_at',
            'updated_at',
            'file',
            'status',
            'registration_address',
            'user',
            'rejection_reason',
        )


class RegistrationWriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=AdminOrCurrentUserDefault())

    class Meta:
        model = Registration
        fields = (
            'file',
            'status',
            'registration_address',
            'user',
        )

    def create(self, validated_data):
        return GetOrCreateDocumentService(Registration, validated_data, self).process()

    def update(self, instance, validated_data):
        user_role = self.context['request'].user.role
        instance = super().update(instance, validated_data)
        ApprovalDocumentService(document=instance, user_role=user_role).process()
        CalculateUserStatusService(instance).process()
        return instance
