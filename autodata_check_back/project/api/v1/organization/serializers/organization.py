from constance import config
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.file.serializers import ImageSerializer
from api.v1.organization.serializers.membership import MembershipReadSerializer
from api.v1.tariffs.serializers import SubscriptionSerializer
from apps.dadata.services import DadataFindByINNService
from apps.file.models import Image
from apps.helpers.serializers import EnumField
from apps.organization.models import Membership, MembershipRoleChoices, Organization, TypeOrganizationChoices
from apps.tariffs.models import Tariff

User = get_user_model()


class CurrentOrganizationDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].organization

    def __repr__(self):
        return '%s()' % self.__class__.__name__  # noqa: WPS323


class OrganizationReadCompactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'title')


class OrganizationReadSerializer(serializers.ModelSerializer):
    type = EnumField(enum_class=TypeOrganizationChoices)
    self_inspection_price = serializers.SerializerMethodField()
    membership = serializers.SerializerMethodField(help_text='Членство в организации')
    num_memberships = serializers.IntegerField(source='users.count', read_only=True, help_text='Кол-во участников')
    num_inspections = serializers.IntegerField(read_only=True, help_text='Кол-во завершенных осмотров')
    avatars = serializers.SerializerMethodField(help_text='Аватарки участников')
    subscriptions = serializers.SerializerMethodField(help_text='Подписки по тарифам')

    class Meta:
        model = Organization
        fields = (
            'id',
            'title',
            'legal_title',
            'is_active',
            'inn',
            'kpp',
            'ogrn',
            'ogrnip',
            'address',
            'type',
            'balance',
            'self_inspection_price',
            'membership',
            'num_memberships',
            'num_inspections',
            'avatars',
            'subscriptions',
        )
        read_only_fields = ('id', 'balance')

    def get_self_inspection_price(self, obj) -> str:
        return str(obj.self_inspection_price) if obj.self_inspection_price else str(config.SELF_INSPECTION_PRICE)

    @swagger_serializer_method(serializer_or_field=MembershipReadSerializer)
    def get_membership(self, obj):
        user = self.context['request'].user
        membership = obj.membership_set.select_related('user').filter(user=user).first()
        return MembershipReadSerializer(membership, context=self.context).data if membership else None

    @swagger_serializer_method(serializer_or_field=ImageSerializer(many=True))
    def get_avatars(self, obj):
        avatars = Image.objects.filter(
            id__in=obj.membership_set.values_list('user__avatar', flat=True).order_by()[:3],
        )
        return ImageSerializer(avatars, many=True, context=self.context).data

    @swagger_serializer_method(serializer_or_field=SubscriptionSerializer(many=True))
    def get_subscriptions(self, obj):
        return SubscriptionSerializer(obj.subscriptions.all(), many=True).data


class OrganizationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            'id',
            'title',
            'legal_title',
            'is_active',
            'inn',
            'kpp',
            'ogrn',
            'ogrnip',
            'address',
            'type',
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = self.context['request'].user
        instance = super().create(validated_data)
        Membership.objects.create(user=user, organization=instance, role=MembershipRoleChoices.OWNER)
        return instance


class OrganizationUpdateSelfInspectionPriceSerializer(serializers.ModelSerializer):  # noqa: WPS118
    class Meta:
        model = Organization
        fields = ('self_inspection_price',)


class OrganizationAdminCompactQuerySerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    membership_role = serializers.ChoiceField(choices=MembershipRoleChoices, required=False)


class OrganizationAdminCompactSerializer(serializers.ModelSerializer):
    membership = serializers.SerializerMethodField(help_text='Членство в организации')
    num_inspections = serializers.IntegerField(read_only=True, help_text='Кол-во завершенных осмотров')
    num_tasks = serializers.IntegerField(read_only=True, help_text='Кол-во заданий')

    class Meta:
        model = Organization
        fields = ('id', 'title', 'membership', 'num_inspections', 'num_tasks')

    @swagger_serializer_method(serializer_or_field=MembershipReadSerializer)
    def get_membership(self, obj):
        query_user = self.context['query_user']
        membership = obj.membership_set.select_related('user').filter(user=query_user).first()
        return MembershipReadSerializer(membership, context=self.context).data if membership else None


class OrganizationCreateForUserRequestSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    title = serializers.CharField(max_length=150, required=False)  # noqa: WPS432
    legal_title = serializers.CharField(max_length=150, required=False)  # noqa: WPS432
    inn = serializers.CharField(max_length=12, required=False)  # noqa: WPS432
    kpp = serializers.CharField(max_length=9, required=False)  # noqa: WPS432
    ogrn = serializers.CharField(max_length=13, required=False)  # noqa: WPS432
    ogrnip = serializers.CharField(max_length=15, required=False)  # noqa: WPS432
    address = serializers.CharField(max_length=500, required=False)  # noqa: WPS432
    type = serializers.ChoiceField(choices=TypeOrganizationChoices, required=False)


class OrganizationCreateForUserSerializer(OrganizationWriteSerializer):
    def create(self, validated_data):
        user = self.context['req_user']
        instance = Organization.objects.create(**validated_data)
        Membership.objects.create(user=user, organization=instance, role=MembershipRoleChoices.OWNER)
        return instance


class ActivateSubscriptionSerializer(serializers.Serializer):
    tariff = serializers.PrimaryKeyRelatedField(queryset=Tariff.objects.all())


class MembershipsOrganizationQuerySerializer(serializers.Serializer):
    only_inspectors = serializers.BooleanField(required=False)


class OrganizationOnlyINNWriteSerializer(serializers.ModelSerializer):
    inn = serializers.CharField(required=True)

    class Meta:
        model = Organization
        fields = ('inn', 'title', 'legal_title', 'kpp', 'ogrn', 'ogrnip', 'address')

    def create(self, validated_data):
        instance = super().create(validated_data)
        user = self.context['request'].user
        Membership.objects.create(user=user, organization=instance, role=MembershipRoleChoices.OWNER)
        return instance


class OrganizationInfoSerializer(serializers.Serializer):
    full_name = serializers.CharField(help_text='Название организации', source='data.name.full_with_opf')
    name = serializers.CharField(help_text='Наименование', source='data.name.short_with_opf')
    ogrn = serializers.CharField(help_text='ОГРН', source='data.ogrn')
    address = serializers.CharField(help_text='Юр. Адрес', source='data.address.value')


class OrganizationChangeBalanceSerializer(serializers.Serializer):
    value = serializers.DecimalField(max_digits=9, decimal_places=2, required=True)
