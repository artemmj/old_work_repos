from django.contrib.auth.password_validation import validate_password
from drf_yasg.utils import swagger_serializer_method
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from api.v1.address.serializers import CitySerializer
from apps.address.managers import CityFilterManager
from apps.address.models import City
from apps.helpers.serializers import EnumField, PointExtField
from apps.user.models import User
from apps.user.models.doc_statuses import UserDocStatuses


class UserCompactSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class UserReadSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField()
    city = CitySerializer()
    location = PointExtField()
    first_name = serializers.SerializerMethodField()
    doc_status = EnumField(enum_class=UserDocStatuses)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'phone',
            'is_self_employed',
            'regions',
            'city',
            'location',
            'doc_status',
        )

    @swagger_serializer_method(serializer_or_field=serializers.CharField())
    def get_first_name(self, instance):
        first_name = instance.first_name
        return first_name if first_name else 'Новый пользователь'


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
            raise ValidationError('Пароли не совпадают')
        return super().validate(attrs)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password1'])
        instance.save()
        return self.instance


class UserWriteSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password2 = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    location = PointExtField(required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'middle_name',
            'last_name',
            'phone',
            'email',
            'password',
            'password2',
            'is_self_employed',
            'city',
            'regions',
            'location',
        )

    def validate_password(self, password):
        validate_password(password)
        return password

    def validate_password2(self, password):
        validate_password(password)
        return password

    def validate(self, attrs):
        if 'password2' in attrs and 'password' in attrs:
            if attrs['password'] != attrs['password2']:
                raise ValidationError('Пароли не совпадают')
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
        instance = super().update(instance, validated_data)

        if 'city' in validated_data:
            instance.regions.clear()
            instance.regions.add(validated_data.get('city').region)
            instance.location = validated_data.get('city').location
        if 'location' in validated_data:
            near_city = CityFilterManager().get_near_city(
                queryset=City.objects.all(),
                location=validated_data.get('location'),
            ).first()
            instance.city = near_city
            instance.regions.clear()
            instance.regions.add(near_city.region)
            instance.location = validated_data.get('location')
        instance.save()

        return instance
