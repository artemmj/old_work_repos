from django.core.validators import MaxLengthValidator, MinLengthValidator
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from apps.user.models import User


class UserRequestCodeWriteSerializer(serializers.Serializer):
    phone = PhoneNumberField()

    class Meta:
        model = User
        fields = ('id', 'phone')


class UserCodeResponseSerializer(serializers.Serializer):
    phone = PhoneNumberField()
    code = serializers.CharField(validators=[MinLengthValidator(6), MaxLengthValidator(6)])
    is_sent = serializers.BooleanField()


class UserRequestLoginSerializer(serializers.Serializer):
    phone = PhoneNumberField()
    code = serializers.CharField(validators=[MinLengthValidator(6), MaxLengthValidator(6)])
