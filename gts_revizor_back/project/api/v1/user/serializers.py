from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from apps.helpers.serializers import EnumField
from apps.user.models import User


class UserReadSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField()

    class Meta:
        model = User
        fields = ('id', 'phone', 'first_name', 'middle_name', 'last_name')


class UserLoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField()


class UserChangePasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def validate_password1(self, password):
        validate_password(password)
        return password

    def validate_password2(self, password):
        validate_password(password)
        return password

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise ValidationError(detail='Пароли не совпадают')
        return super().validate(attrs)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password1'])
        instance.save()
        return self.instance


class UserWriteSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(validators=[UniqueValidator(queryset=User.objects.all())])
    password2 = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'phone', 'password', 'password2')
        read_only_fields = ('id',)

    def validate_password(self, password):
        validate_password(password)
        return password

    def validate_password2(self, password):
        validate_password(password)
        return password

    def validate(self, attrs):
        if 'password2' in attrs and 'password' in attrs:
            if attrs['password'] != attrs['password2']:
                raise ValidationError(detail='Пароли не совпадают')
        return super().validate(attrs)

    def create(self, validated_data):
        password2 = validated_data.pop('password2')

        user = User.objects.create(**validated_data)
        user.set_password(password2)
        user.save()

        return user

    def update(self, instance, validated_data):
        if 'password2' in validated_data and 'password' in validated_data:
            validated_data.pop('password2')
            password = validated_data.pop('password')
            instance.set_password(password)
            instance.save()

        return super().update(instance, validated_data)
