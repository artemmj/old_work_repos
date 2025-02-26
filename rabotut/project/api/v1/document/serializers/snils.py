from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.document.helpers import AdminOrCurrentUserDefault
from apps.document.models import Snils
from apps.document.models.snils.validators import SNILSValidator
from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.document.services import (
    ApprovalDocumentService,
    CalculateUserStatusService,
    GetOrCreateDocumentService,
    ValidateRequestUserDocumentService,
)
from apps.helpers.serializers import EnumField

from .mixins import ListFileFieldMixin

User = get_user_model()


class SnilsReadSerializer(serializers.ModelSerializer, ListFileFieldMixin):
    file = serializers.SerializerMethodField()  # noqa: WPS110
    status = EnumField(enum_class=BaseUserDocumentStatuses)

    class Meta:
        model = Snils
        fields = (
            'id',
            'created_at',
            'updated_at',
            'value',
            'status',
            'file',
            'user',
            'rejection_reason',
        )


class SnilsWriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=AdminOrCurrentUserDefault())
    value = serializers.CharField()  # noqa: WPS110

    class Meta:
        model = Snils
        fields = (
            'value',
            'file',
            'user',
        )

    def validate_value(self, value):  # noqa: WPS110
        SNILSValidator()(value)
        ValidateRequestUserDocumentService().process(
            model=Snils,
            value=value,
            request_user=self.context['request'].user,
        )
        return value

    def create(self, validated_data):
        return GetOrCreateDocumentService(Snils, validated_data, self).process()

    def update(self, instance, validated_data):
        user_role = self.context['request'].user.role
        instance = super().update(instance, validated_data)
        ApprovalDocumentService(document=instance, user_role=user_role).process()
        CalculateUserStatusService(instance).process()
        return instance
