from rest_framework import serializers

from api.v1.departaments.serializers import DepartmentSerializer
from api.v1.projects.serializers import ProjectSerializer
from api.v1.regions.serializers import RegionSerializer
from apps.departments.models import Department
from apps.helpers.serializers import EnumField
from apps.projects.models import Project
from apps.regions.models import Region
from apps.survey.models import BaseSurveyMailing, UserRolesChoices

from .survey import SurveyRetrieveSerializer


class SurveyMailingSwaggerSerializer(serializers.ModelSerializer):
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
            'SurveyMailingDepartments',
            'SurveyMailingRegions',
            'SurveyMailingProjects',
            'SurveyMailingRoles',
        ),
        required=True,
    )

    class Meta:
        model = BaseSurveyMailing
        fields = (
            'id',
            'survey',
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


class SurveyMailingRetrieveSwaggerSerializer(SurveyMailingSwaggerSerializer):
    survey = SurveyRetrieveSerializer()
    departments = DepartmentSerializer(many=True, required=False)
    regions = RegionSerializer(many=True, required=False)
    projects = ProjectSerializer(many=True, required=False)
    roles = EnumField(enum_class=UserRolesChoices, required=False)
    to_all_regions = serializers.BooleanField(required=False)

    class Meta:
        model = BaseSurveyMailing
        fields = (
            'id',
            'survey',
            'is_published',
            'is_push',
            'departments',
            'regions',
            'projects',
            'roles',
            'to_all_regions',
            'resourcetype',
        )


class SurveyMailingUpdateSwaggerSerializer(SurveyMailingSwaggerSerializer):
    departments = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), many=True, required=False)
    regions = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(), many=True, required=False)
    projects = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), many=True, required=False)
    roles = serializers.ListField(
        child=serializers.ChoiceField(choices=UserRolesChoices),
        required=False,
    )
    to_all_regions = serializers.BooleanField(required=False)

    class Meta:
        model = BaseSurveyMailing
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
