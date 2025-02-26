from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.document.helpers import AdminOrCurrentUserDefault
from apps.document.models import Selfie, SelfieRecognition, SelfieStatuses
from apps.document.models.passport.passport import Passport
from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.document.services import (
    ApprovalDocumentService,
    CalculateUserStatusService,
    GetOrCreateDocumentService,
    VerifySelfiePassportService,
)
from apps.helpers.serializers import EnumField

from .mixins import ListFileFieldMixin

User = get_user_model()


class RecognitionResultSerializer(serializers.Serializer):
    faces_is_detected = serializers.BooleanField()
    faces_is_equal = serializers.BooleanField(allow_null=True)
    probability = serializers.CharField()
    probability_value = serializers.FloatField()
    result = serializers.BooleanField()  # noqa: WPS110
    success_call = serializers.BooleanField()
    error = serializers.CharField()


class SelfieRecognitionSerializer(serializers.ModelSerializer):
    recognition_result = RecognitionResultSerializer()
    status = EnumField(enum_class=SelfieStatuses)

    class Meta:
        model = SelfieRecognition
        fields = (
            'passport',
            'recognition_result',
            'status',
            'match_confirmation',
        )


class SelfieReadSerializer(serializers.ModelSerializer, ListFileFieldMixin):
    recognitions = SelfieRecognitionSerializer(many=True)
    file = serializers.SerializerMethodField()  # noqa: WPS110
    status = EnumField(enum_class=BaseUserDocumentStatuses)

    class Meta:
        model = Selfie
        fields = (
            'id',
            'created_at',
            'updated_at',
            'file',
            'user',
            'status',
            'rejection_reason',
            'recognitions',
        )


class SelfieWriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=AdminOrCurrentUserDefault())

    class Meta:
        model = Selfie
        fields = (
            'id',
            'file',
            'status',
            'user',
        )

    def create(self, validated_data):
        selfie = GetOrCreateDocumentService(Selfie, validated_data, self).process()
        VerifySelfiePassportService(selfie).process()
        return selfie

    def update(self, instance, validated_data):
        user_role = self.context['request'].user.role
        instance = super().update(instance, validated_data)
        ApprovalDocumentService(document=instance, user_role=user_role).process()
        CalculateUserStatusService(instance).process()
        return instance


class AcceptPassportSerializer(serializers.Serializer):
    passport = serializers.PrimaryKeyRelatedField(queryset=Passport.objects.all())
