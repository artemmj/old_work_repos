from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_serializer_method
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt import serializers as jwt_serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.file.serializers import ImageSerializer
from apps.helpers.checking_sms_code import checking_code
from apps.helpers.custom_error import CustomValidationError
from apps.helpers.exceptions import AuthenticationFailed
from apps.helpers.registration_validators import agreement_validator, username_validator
from apps.helpers.serializers import EagerLoadingSerializerMixin, EnumField
from apps.inspection.models.inspection import Inspection, StatusChoices
from apps.inspection_task.models.task import InspectionTask, InspectorTaskStatuses
from apps.organization.models import Membership, MembershipRoleChoices, Organization
from apps.organization.models.preparatory_invitation import PreparatoryInvitation
from apps.user.models import ConfirmationCode, RoleChoices, User


class CustomInvalidToken(AuthenticationFailed):
    status_code = status.HTTP_400_BAD_REQUEST


class CustomTokenObtainPairSerializer(jwt_serializers.TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        if user:
            token = super().get_token(user)
            return token  # noqa: WPS331
        raise CustomInvalidToken('not_found!')

    def validate(self, attrs):
        user = get_object_or_404(User, phone=attrs['phone'])
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass  # noqa:  WPS420

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise AuthenticationFailed()

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class UserCompactSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    avatar = ImageSerializer(required=False)

    select_related_fields = ('avatar',)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone', 'avatar')


class UserAdminCompactSerializer(serializers.ModelSerializer):
    is_inspector = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone', 'is_inspector')

    def get_is_inspector(self, obj) -> bool:
        return True if RoleChoices.INSPECTOR in obj.roles else False  # noqa: WPS502


class OrganizationForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'title')


class MembershipForUserSerializer(serializers.ModelSerializer):
    role = EnumField(enum_class=MembershipRoleChoices)
    organization = serializers.SerializerMethodField()

    class Meta:
        model = Membership
        fields = (
            'id',
            'created_at',
            'organization',
            'role',
            'is_active',
        )

    @swagger_serializer_method(serializer_or_field=OrganizationForUserSerializer)
    def get_organization(self, obj):
        return OrganizationForUserSerializer(obj.organization).data


class UserReadSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    phone = PhoneNumberField()
    avatar = ImageSerializer(required=False)
    roles = serializers.ListField(child=EnumField(enum_class=RoleChoices))
    is_inspector = serializers.SerializerMethodField()
    active_organization_membership = serializers.SerializerMethodField(help_text='Активная организация')
    num_tasks = serializers.SerializerMethodField()
    num_inspections = serializers.SerializerMethodField()

    select_related_fields = ('avatar',)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'phone',
            'avatar',
            'agreement_policy',
            'agreement_processing',
            'roles',
            'is_inspector',
            'created_at',
            'active_organization_membership',
            'num_tasks',
            'num_inspections',
        )

    def get_is_inspector(self, obj) -> bool:
        return True if RoleChoices.INSPECTOR in obj.roles else False  # noqa: WPS502

    @swagger_serializer_method(serializer_or_field=MembershipForUserSerializer)
    def get_active_organization_membership(self, obj):
        active_organization = obj.membership_set.filter(is_active=True).first()
        return MembershipForUserSerializer(active_organization).data

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_num_tasks(self, instance):
        return InspectionTask.objects.filter(inspector=instance).exclude(status=InspectorTaskStatuses.DRAFT).count()

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_num_inspections(self, instance):
        return Inspection.objects.filter(inspector=instance, status=StatusChoices.COMPLETE).count()


class UserWriteSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(validators=[UniqueValidator(queryset=User.objects.all())])
    password2 = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    first_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    middle_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'phone', 'password', 'password2', 'avatar', 'first_name', 'middle_name', 'last_name')
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


class UserCreateSerializer(UserWriteSerializer):
    role = serializers.ChoiceField(choices=RoleChoices.choices, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = PhoneNumberField(validators=[UniqueValidator(queryset=User.objects.all())], required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('role', 'phone', 'first_name', 'last_name', 'password', 'password2')

    def create(self, validated_data):
        password2 = validated_data.pop('password2')
        role = validated_data.pop('role')
        user = User.objects.create(**validated_data)
        user.roles = [role]
        user.set_password(password2)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'phone',
        )

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():  # noqa: WPS110
            setattr(instance, attr, value)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    phone = PhoneNumberField()
    password = serializers.CharField()


class UserRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    middle_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    phone = PhoneNumberField(validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    password = serializers.CharField(write_only=True, required=True)
    agreement_processing = serializers.BooleanField(default=True)
    agreement_policy = serializers.BooleanField(default=True)
    code = serializers.CharField(required=True, min_length=4, max_length=4)

    validators = [agreement_validator, username_validator]

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'middle_name',
            'last_name',
            'phone',
            'agreement_processing',
            'agreement_policy',
        )

    def validate(self, attrs):
        if len(attrs['password']) < 8:
            raise ValidationError({'password': ['Длина пароля меньше 8 символов']})
        phone = attrs.get('phone')
        code = attrs.get('code')
        checking_code(phone, code)
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('code')
        if validated_data['password']:
            validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)

        prepare_invs = PreparatoryInvitation.objects.filter(is_active=True, phone=validated_data.get('phone'))
        if prepare_invs:
            prepare_invs.update(is_active=False)
            last_inv = prepare_invs.order_by('-created_at').first()
            Membership.objects.create(
                user=user,
                organization=last_inv.organization,
                role=MembershipRoleChoices.INSPECTOR,
            )

        return user


class ConfirmCodeSerializer(serializers.Serializer):
    phone = PhoneNumberField(required=True)
    code = serializers.CharField(required=True, min_length=4, max_length=4)

    def validate(self, attrs):  # noqa: WPS238
        phone = attrs.get('phone')
        code = attrs.get('code')
        checking_code(phone, code)
        return attrs


class PasswordResetByCodeSerializer(serializers.Serializer):
    phone = PhoneNumberField(required=True)
    code = serializers.CharField(required=True, min_length=4, max_length=4)
    password = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return self.instance

    def validate(self, attrs):
        validate_password(attrs.get('password'))
        phone = attrs.get('phone')
        code = attrs.get('code')
        get_object_or_404(User, phone=phone)
        checking_code(phone, code)
        return super().validate(attrs)


class UserChangePasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        validate_password(attrs['password1'])
        validate_password(attrs['password2'])

        if attrs['password1'] != attrs['password2']:
            raise ValidationError(detail='Пароли не совпадают')
        return super().validate(attrs)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password1'])
        instance.save()
        return self.instance


class SendCodeRegistrationSerializer(serializers.Serializer):
    phone = PhoneNumberField(label='Номер телефона', help_text='+79270000000', required=True)

    def validate(self, attrs):
        phone = attrs['phone']

        if User.objects.filter(phone=phone).exists():
            raise CustomValidationError(
                {'phone': ['Ваш номер уже зарегистрован в системе']},
                status_code=status.HTTP_409_CONFLICT,
            )
        return attrs

    def save(self, validated_data):
        ConfirmationCode.objects.create(phone=validated_data['phone'])


class SendCodeSerializer(serializers.Serializer):
    phone = PhoneNumberField(label='Номер телефона', help_text='+79270000000', required=True)

    def save(self, validated_data):
        phone = validated_data.get('phone')
        if not User.objects.filter(phone=phone).exists():
            raise ValidationError({'phone': ['Указанный номер не зарегистрирован. Необходимо пройти регистрацию']})

        ConfirmationCode.objects.create(phone=phone)
