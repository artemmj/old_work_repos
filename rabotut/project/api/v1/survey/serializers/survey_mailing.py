from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_polymorphic.serializers import PolymorphicSerializer

from api.v1.departaments.serializers import DepartmentSerializer
from api.v1.projects.serializers import ProjectSerializer
from api.v1.regions.serializers import RegionSerializer
from apps.helpers.serializers import EnumSerializer
from apps.regions.models import Region
from apps.survey.models import (
    BaseSurveyMailing,
    SurveyMailingDepartments,
    SurveyMailingProjects,
    SurveyMailingRegions,
    SurveyMailingRoles,
    UserRolesChoices,
)

from .survey import SurveyRetrieveSerializer


class BaseSurveyMailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseSurveyMailing
        fields = ('id', 'survey', 'publish_datetime', 'is_published', 'is_push')
        read_only_fields = ('id',)


class BaseSurveyMailingListSerializer(serializers.ModelSerializer):
    survey = SurveyRetrieveSerializer()

    class Meta:
        model = BaseSurveyMailing
        fields = ('id', 'survey', 'publish_datetime', 'is_published', 'is_push')


class SurveyMailingDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyMailingDepartments
        fields = ('id', 'survey', 'publish_datetime', 'is_published', 'is_push', 'departments')
        read_only_fields = ('id',)


class SurveyMailingDepartmentRetrieveSerializer(serializers.ModelSerializer):
    survey = SurveyRetrieveSerializer()
    departments = DepartmentSerializer(many=True)

    class Meta:
        model = SurveyMailingDepartments
        fields = ('id', 'survey', 'publish_datetime', 'is_published', 'is_push', 'departments')


class SurveyMailingRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyMailingRegions
        fields = ('id', 'survey', 'publish_datetime', 'is_published', 'is_push', 'regions', 'to_all_regions')
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


class SurveyMailingRegionRetrieveSerializer(serializers.ModelSerializer):
    survey = SurveyRetrieveSerializer()
    regions = RegionSerializer(many=True)

    class Meta:
        model = SurveyMailingRegions
        fields = ('id', 'survey', 'publish_datetime', 'is_published', 'is_push', 'regions')
        read_only_fields = ('id',)


class SurveyMailingProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyMailingProjects
        fields = ('id', 'survey', 'publish_datetime', 'is_published', 'is_push', 'projects')
        read_only_fields = ('id',)


class SurveyMailingProjectRetrieveSerializer(serializers.ModelSerializer):
    survey = SurveyRetrieveSerializer()
    projects = ProjectSerializer(many=True)

    class Meta:
        model = SurveyMailingProjects
        fields = ('id', 'survey', 'publish_datetime', 'is_published', 'is_push', 'projects')
        read_only_fields = ('id',)


class SurveyMailingUserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyMailingRoles
        fields = ('id', 'survey', 'publish_datetime', 'is_published', 'is_push', 'roles')
        read_only_fields = ('id',)


class SurveyMailingUserRoleRetrieveSerializer(serializers.ModelSerializer):
    survey = SurveyRetrieveSerializer()
    roles = serializers.SerializerMethodField()

    class Meta:
        model = SurveyMailingRoles
        fields = ('id', 'survey', 'publish_datetime', 'is_published', 'is_push', 'roles')
        read_only_fields = ('id',)

    def get_roles(self, obj):  # noqa: WPS110
        roles = [UserRolesChoices[role.upper()] for role in obj.roles]
        return EnumSerializer(roles, many=True).data


class SurveyMailingPolymorphicSerializer(PolymorphicSerializer):
    base_serializer_class = BaseSurveyMailingSerializer
    model_serializer_mapping = {
        SurveyMailingDepartments: SurveyMailingDepartmentSerializer,
        SurveyMailingRegions: SurveyMailingRegionSerializer,
        SurveyMailingProjects: SurveyMailingProjectSerializer,
        SurveyMailingRoles: SurveyMailingUserRoleSerializer,
    }

    def update(self, instance, validated_data):
        if instance.is_published:
            raise ValidationError('Опрос уже опубликован.')
        return super().update(instance, validated_data)


class SurveyMailingRetrievePolymorphicSerializer(PolymorphicSerializer):
    base_serializer_class = BaseSurveyMailingSerializer
    model_serializer_mapping = {
        SurveyMailingDepartments: SurveyMailingDepartmentRetrieveSerializer,
        SurveyMailingRegions: SurveyMailingRegionRetrieveSerializer,
        SurveyMailingProjects: SurveyMailingProjectRetrieveSerializer,
        SurveyMailingRoles: SurveyMailingUserRoleRetrieveSerializer,
    }
