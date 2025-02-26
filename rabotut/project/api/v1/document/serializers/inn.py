from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.document.helpers import AdminOrCurrentUserDefault
from apps.document.models import Inn
from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.document.services import (
    ApprovalDocumentService,
    CalculateUserStatusService,
    GetOrCreateDocumentService,
    ValidateRequestUserDocumentService,
)
from apps.helpers.serializers import EnumField
from apps.user.validators import InnValidator

from .mixins import ListFileFieldMixin

User = get_user_model()


class InnReadSerializer(serializers.ModelSerializer, ListFileFieldMixin):
    file = serializers.SerializerMethodField()  # noqa: WPS110
    status = EnumField(enum_class=BaseUserDocumentStatuses)

    class Meta:
        model = Inn
        fields = (
            'id',
            'created_at',
            'updated_at',
            'value',
            'verification_at',
            'is_self_employed',
            'is_manual_verification_required',
            'file',
            'user',
            'status',
            'rejection_reason',
        )


class InnWriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=AdminOrCurrentUserDefault())
    value = serializers.CharField()  # noqa: WPS110

    class Meta:
        model = Inn
        fields = (
            'value',
            'verification_at',
            'is_self_employed',
            'is_manual_verification_required',
            'file',
            'user',
            'status',
        )

    def validate_value(self, value):  # noqa: WPS110
        InnValidator()(value)
        request_user = self.context['request'].user
        ValidateRequestUserDocumentService().process(model=Inn, value=value, request_user=request_user)
        return value

    def create(self, validated_data):
        return GetOrCreateDocumentService(Inn, validated_data, self).process()

    def update(self, instance, validated_data):
        user_role = self.context['request'].user.role
        instance = super().update(instance, validated_data)
        ApprovalDocumentService(document=instance, user_role=user_role).process()
        CalculateUserStatusService(instance).process()
        return instance
