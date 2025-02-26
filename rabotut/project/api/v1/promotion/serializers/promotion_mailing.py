from drf_yasg.utils import swagger_serializer_method  # noqa: WPS202
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_polymorphic.serializers import PolymorphicSerializer

from api.v1.departaments.serializers import DepartmentSerializer
from api.v1.projects.serializers import ProjectSerializer
from api.v1.regions.serializers import RegionSerializer
from apps.departments.models import Department
from apps.helpers.serializers import EnumField, EnumSerializer
from apps.projects.models import Project
from apps.promotion.models import (
    BasePromotionMailing,
    PromotionMailingDepartment,
    PromotionMailingProject,
    PromotionMailingRegion,
    PromotionMailingUserRole,
    UserRolesChoices,
)
from apps.regions.models import Region

from .promotion import PromotionRetrieveSerializer, PromotionSerializer


class BasePromotionMailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasePromotionMailing
        fields = ('id', 'promotion', 'publish_datetime', 'is_published', 'is_push')
        read_only_fields = ('id',)


class BasePromotionMailingListSerializer(BasePromotionMailingSerializer):
    promotion = PromotionSerializer()

    class Meta:
        model = BasePromotionMailing
        fields = ('id', 'promotion', 'publish_datetime', 'is_published', 'is_push')


class PromotionMailingDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionMailingDepartment
        fields = ('id', 'promotion', 'publish_datetime', 'departments', 'is_published', 'is_push')
        read_only_fields = ('id',)


class PromotionMailingDepartmentRetrieveSerializer(serializers.ModelSerializer):
    promotion = PromotionRetrieveSerializer()
    departments = DepartmentSerializer(many=True)

    class Meta:
        model = PromotionMailingDepartment
        fields = ('id', 'promotion', 'publish_datetime', 'departments', 'is_published', 'is_push')


class PromotionMailingRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionMailingRegion
        fields = ('id', 'promotion', 'publish_datetime', 'regions', 'is_published', 'is_push', 'to_all_regions')
        read_only_fields = ('id',)
        extra_kwargs = {
            'regions': {'allow_empty': True},
        }

    def validate(self, attrs):
        if attrs.get('to_all_regions'):
            attrs['regions'] = Region.objects.all().values_list('id', flat=True)
        elif not attrs['regions']:
            raise ValidationError({'regions': 'Для рассылки по регионам требуются регионы.'})
        return attrs


class PromotionMailingRegionRetrieveSerializer(serializers.ModelSerializer):
    promotion = PromotionRetrieveSerializer()
    regions = RegionSerializer(many=True)

    class Meta:
        model = PromotionMailingRegion
        fields = ('id', 'promotion', 'publish_datetime', 'regions', 'is_published', 'is_push', 'to_all_regions')
        read_only_fields = ('id',)


class PromotionMailingProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionMailingProject
        fields = ('id', 'promotion', 'publish_datetime', 'projects', 'is_published', 'is_push')
        read_only_fields = ('id',)


class PromotionMailingProjectRetrieveSerializer(serializers.ModelSerializer):
    promotion = PromotionRetrieveSerializer()
    projects = ProjectSerializer(many=True)

    class Meta:
        model = PromotionMailingProject
        fields = ('id', 'promotion', 'publish_datetime', 'projects', 'is_published', 'is_push')
        read_only_fields = ('id',)


class PromotionMailingUserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionMailingUserRole
        fields = ('id', 'promotion', 'publish_datetime', 'roles', 'is_published', 'is_push')
        read_only_fields = ('id',)


class PromotionMailingUserRoleRetrieveSerializer(serializers.ModelSerializer):
    promotion = PromotionRetrieveSerializer()
    roles = serializers.SerializerMethodField()

    class Meta:
        model = PromotionMailingUserRole
        fields = ('id', 'promotion', 'publish_datetime', 'roles', 'is_published', 'is_push')
        read_only_fields = ('id',)

    @swagger_serializer_method(serializer_or_field=EnumSerializer(many=True))
    def get_roles(self, obj):  # noqa: WPS110
        roles = [UserRolesChoices[role.upper()] for role in obj.roles]
        return EnumSerializer(roles, many=True).data


class PromotionMailingPolymorphicSerializer(PolymorphicSerializer):
    base_serializer_class = BasePromotionMailingSerializer
    model_serializer_mapping = {
        PromotionMailingDepartment: PromotionMailingDepartmentSerializer,
        PromotionMailingRegion: PromotionMailingRegionSerializer,
        PromotionMailingProject: PromotionMailingProjectSerializer,
        PromotionMailingUserRole: PromotionMailingUserRoleSerializer,
    }

    def update(self, instance, validated_data):
        if instance.is_published:
            raise ValidationError('Новость уже опубликована.')
        return super().update(instance, validated_data)


class PromotionMailingRetrievePolymorphicSerializer(PolymorphicSerializer):
    base_serializer_class = BasePromotionMailingSerializer
    model_serializer_mapping = {
        PromotionMailingDepartment: PromotionMailingDepartmentRetrieveSerializer,
        PromotionMailingRegion: PromotionMailingRegionRetrieveSerializer,
        PromotionMailingProject: PromotionMailingProjectRetrieveSerializer,
        PromotionMailingUserRole: PromotionMailingUserRoleRetrieveSerializer,
    }


class PromotionMailingSwaggerSerializer(serializers.ModelSerializer):
    departments = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), many=True, required=False)
    regions = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(), many=True, required=False)
    projects = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), many=True, required=False)
    roles = serializers.ListField(
        child=serializers.ChoiceField(choices=UserRolesChoices),
        required=False,
    )
    to_all_regions = serializers.BooleanField(required=False)

    resourcetype = serializers.ChoiceField(
        choices=(
            'PromotionMailingDepartment',
            'PromotionMailingRegion',
            'PromotionMailingProject',
            'PromotionMailingUserRole',
        ),
        required=True,
    )

    class Meta:
        model = BasePromotionMailing
        fields = (
            'id',
            'promotion',
            'publish_datetime',
            'is_published',
            'is_push',
            'departments',
            'regions',
            'projects',
            'roles',
            'resourcetype',
            'to_all_regions',
        )
        read_only_fields = ('id',)


class PromotionMailingRetrieveSwaggerSerializer(PromotionMailingSwaggerSerializer):
    promotion = PromotionRetrieveSerializer()
    departments = DepartmentSerializer(many=True, required=False)
    regions = RegionSerializer(many=True, required=False)
    projects = ProjectSerializer(many=True, required=False)
    roles = EnumField(enum_class=UserRolesChoices, required=False)
    to_all_regions = serializers.BooleanField(required=False)

    class Meta:
        model = BasePromotionMailing
        fields = (
            'id',
            'promotion',
            'is_published',
            'is_push',
            'departments',
            'regions',
            'projects',
            'roles',
            'to_all_regions',
            'resourcetype',
        )


class PromotionMailingUpdateSwaggerSerializer(PromotionMailingSwaggerSerializer):
    departments = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), many=True, required=False)
    regions = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(), many=True, required=False)
    projects = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), many=True, required=False)
    roles = serializers.ListField(
        child=serializers.ChoiceField(choices=UserRolesChoices),
        required=False,
    )
    to_all_regions = serializers.BooleanField(required=False)

    class Meta:
        model = BasePromotionMailing
        fields = (
            'id',
            'is_published',
            'is_push',
            'departments',
            'regions',
            'projects',
            'roles',
            'to_all_regions',
        )
