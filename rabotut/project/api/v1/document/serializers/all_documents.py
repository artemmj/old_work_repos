from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.helpers.serializers import EnumField, EnumSerializer

from ..serializers import (
    InnReadSerializer,
    PassportReadSerializer,
    RegistrationReadSerializer,
    SelfieReadSerializer,
    SnilsReadSerializer,
)


class AllDocPassportReadSerializer(PassportReadSerializer):
    status = EnumField(enum_class=BaseUserDocumentStatuses)


class AllDocInnReadSerializer(InnReadSerializer):
    status = EnumField(enum_class=BaseUserDocumentStatuses)


class AllDocSnilsReadSerializer(SnilsReadSerializer):
    status = EnumField(enum_class=BaseUserDocumentStatuses)


class AllDocRegistrationReadSerializer(RegistrationReadSerializer):
    status = EnumField(enum_class=BaseUserDocumentStatuses)


class AllDocSelfieReadSerializer(SelfieReadSerializer):
    status = EnumField(enum_class=BaseUserDocumentStatuses)


class AllDocumentsSerializer(serializers.Serializer):
    passport = AllDocPassportReadSerializer(many=True, required=False)
    inn = AllDocInnReadSerializer(many=True, required=False)
    snils = AllDocSnilsReadSerializer(many=True, required=False)
    registration = AllDocRegistrationReadSerializer(many=True, required=False)
    selfie = AllDocSelfieReadSerializer(many=True, required=False)
    status = EnumSerializer()


class QueryAllDocumentsSerializer(serializers.Serializer):
    user_phone = PhoneNumberField(required=False)


class DeclineDocumentSerializer(serializers.Serializer):
    rejection_reason = serializers.CharField(required=True)
