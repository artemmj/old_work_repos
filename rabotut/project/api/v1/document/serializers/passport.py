from dateutil.relativedelta import relativedelta
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.document.helpers import AdminOrCurrentUserDefault
from apps.document.models import Passport
from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.document.services import (
    ApprovalDocumentService,
    CalculateUserStatusService,
    GetOrCreateDocumentService,
    PassportCheckExrationService,
    ValidateRequestUserDocumentService,
)
from apps.helpers.serializers import EnumField
from apps.helpers.services import ServiceError

from .mixins import ListFileFieldMixin

MIN_REGISRATION_AGE = 18


class PassportReadSerializer(serializers.ModelSerializer, ListFileFieldMixin):
    file = serializers.SerializerMethodField()  # noqa: WPS110
    status = EnumField(enum_class=BaseUserDocumentStatuses)

    class Meta:
        model = Passport
        fields = (
            'id',
            'created_at',
            'updated_at',
            'first_name',
            'last_name',
            'patronymic',
            'gender',
            'birth_date',
            'place_of_birth',
            'citizenship',
            'number',
            'series',
            'department_code',
            'date_issue',
            'issued_by',
            'file',
            'user',
            'status',
            'rejection_reason',
        )


class PassportWriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=AdminOrCurrentUserDefault())

    class Meta:
        model = Passport
        fields = (
            'user',
            'status',
            'gender',
            'birth_date',
            'place_of_birth',
            'citizenship',
            'number',
            'series',
            'department_code',
            'date_issue',
            'issued_by',
            'first_name',
            'last_name',
            'patronymic',
            'file',
        )
        extra_kwargs = {
            'file': {'required': True},
            'citizenship': {'required': False},
        }

    def validate_number(self, value):  # noqa: WPS110
        request_user = self.context['request'].user
        ValidateRequestUserDocumentService().process(model=Passport, value=value, request_user=request_user)
        return value

    def validate_birth_date(self, birth_date):
        years = relativedelta(timezone.now().date(), birth_date).years
        if years < MIN_REGISRATION_AGE:
            raise ValidationError('Ваш возраст меньше 18 лет. Работа в приложении недоступна.')
        return birth_date

    def validate_date_issue(self, date_issue):
        birth_date = self.initial_data.get('birth_date', self.instance and self.instance.birth_date)
        try:
            PassportCheckExrationService().process(birth_date, date_issue)
        except ServiceError as e:
            raise ValidationError(str(e))
        return date_issue

    def create(self, validated_data):
        return GetOrCreateDocumentService(Passport, validated_data, self).process()

    def update(self, instance, validated_data):
        user_role = self.context['request'].user.role
        instance = super().update(instance, validated_data)
        ApprovalDocumentService(document=instance, user_role=user_role).process()
        CalculateUserStatusService(instance).process()
        return instance


class PassportRecognitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        fields = ('file',)


class PassportRecognitionResponseSerializer(serializers.Serializer):
    gender = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    patronymic = serializers.CharField()
    birth_date = serializers.CharField()
    citizenship = serializers.CharField()
    number = serializers.CharField()
    series = serializers.CharField()
    department_code = serializers.CharField()
    date_issue = serializers.CharField()
    issued_by = serializers.CharField()
    place_of_birth = serializers.CharField()
