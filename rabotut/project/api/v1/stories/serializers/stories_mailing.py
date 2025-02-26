from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_polymorphic.serializers import PolymorphicSerializer

from api.v1.departaments.serializers import DepartmentSerializer
from api.v1.projects.serializers import ProjectSerializer
from api.v1.regions.serializers import RegionSerializer
from api.v1.stories.serializers.stories import StoriesRetrieveSerializer
from apps.departments.models import Department
from apps.helpers.serializers import EnumField, EnumSerializer
from apps.news.models import UserRolesChoices
from apps.projects.models import Project
from apps.regions.models import Region
from apps.stories.models import (
    BaseStoriesMailing,
    StoriesMailingDepartment,
    StoriesMailingProject,
    StoriesMailingRegion,
    StoriesMailingUserRole,
)


class BaseStoriesMailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseStoriesMailing
        fields = ('id', 'stories', 'publish_datetime', 'is_published', 'is_push')
        read_only_fields = ('id',)


class BaseStoriesMailingListSerializer(BaseStoriesMailingSerializer):
    stories = StoriesRetrieveSerializer()

    class Meta:
        model = BaseStoriesMailing
        fields = ('id', 'stories', 'publish_datetime', 'is_published', 'is_push')


class StoriesMailingDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoriesMailingDepartment
        fields = ('id', 'stories', 'publish_datetime', 'departments', 'is_published', 'is_push')
        read_only_fields = ('id',)


class StoriesMailingDepartmentRetrieveSerializer(serializers.ModelSerializer):
    stories = StoriesRetrieveSerializer()
    departments = DepartmentSerializer(many=True)

    class Meta:
        model = StoriesMailingDepartment
        fields = ('id', 'stories', 'publish_datetime', 'departments', 'is_published', 'is_push')
        read_only_fields = ('id',)


class StoriesMailingRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoriesMailingRegion
        fields = ('id', 'stories', 'publish_datetime', 'regions', 'is_published', 'is_push', 'to_all_regions')
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


class StoriesMailingRegionRetrieveSerializer(serializers.ModelSerializer):
    stories = StoriesRetrieveSerializer()
    regions = RegionSerializer(many=True)

    class Meta:
        model = StoriesMailingRegion
        fields = ('id', 'stories', 'publish_datetime', 'regions', 'is_published', 'is_push', 'to_all_regions')
        read_only_fields = ('id',)


class StoriesMailingProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoriesMailingProject
        fields = ('id', 'stories', 'publish_datetime', 'projects', 'is_published', 'is_push')
        read_only_fields = ('id',)


class StoriesMailingProjectRetrieveSerializer(serializers.ModelSerializer):
    stories = StoriesRetrieveSerializer()
    projects = ProjectSerializer(many=True)

    class Meta:
        model = StoriesMailingProject
        fields = ('id', 'stories', 'publish_datetime', 'projects', 'is_published', 'is_push')
        read_only_fields = ('id',)


class StoriesMailingUserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoriesMailingUserRole
        fields = ('id', 'stories', 'publish_datetime', 'roles', 'is_published', 'is_push')
        read_only_fields = ('id',)


class StoriesMailingUserRoleRetrieveSerializer(serializers.ModelSerializer):
    stories = StoriesRetrieveSerializer()
    roles = serializers.SerializerMethodField()

    class Meta:
        model = StoriesMailingUserRole
        fields = ('id', 'stories', 'publish_datetime', 'roles', 'is_published', 'is_push')
        read_only_fields = ('id',)

    @swagger_serializer_method(serializer_or_field=EnumSerializer(many=True))
    def get_roles(self, obj):  # noqa: WPS110
        roles = [UserRolesChoices[role.upper()] for role in obj.roles]
        return EnumSerializer(roles, many=True).data


class StoriesMailingPolymorphicSerializer(PolymorphicSerializer):
    base_serializer_class = BaseStoriesMailingSerializer
    model_serializer_mapping = {
        StoriesMailingDepartment: StoriesMailingDepartmentSerializer,
        StoriesMailingRegion: StoriesMailingRegionSerializer,
        StoriesMailingProject: StoriesMailingProjectSerializer,
        StoriesMailingUserRole: StoriesMailingUserRoleSerializer,
    }

    def update(self, instance, validated_data):
        if instance.is_published:
            raise ValidationError('Сторис уже опубликована.')
        return super().update(instance, validated_data)


class StoriesMailingRetrievePolymorphicSerializer(PolymorphicSerializer):
    base_serializer_class = BaseStoriesMailingSerializer
    model_serializer_mapping = {
        StoriesMailingDepartment: StoriesMailingDepartmentRetrieveSerializer,
        StoriesMailingRegion: StoriesMailingRegionRetrieveSerializer,
        StoriesMailingProject: StoriesMailingProjectRetrieveSerializer,
        StoriesMailingUserRole: StoriesMailingUserRoleRetrieveSerializer,
    }


class StoriesMailingSwaggerSerializer(serializers.ModelSerializer):
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
            'StoriesMailingDepartment',
            'StoriesMailingRegion',
            'StoriesMailingProject',
            'StoriesMailingUserRoleSerializer',
        ),
        required=True,
    )

    class Meta:
        model = BaseStoriesMailing
        fields = (
            'id',
            'stories',
            'publish_datetime',
            'is_published',
            'is_push',
            'departments',
            'regions',
            'projects',
            'roles',
            'to_all_regions',
            'resourcetype',
        )
        read_only_fields = ('id',)


class StoriesMailingRetrieveSwaggerSerializer(StoriesMailingSwaggerSerializer):
    stories = StoriesRetrieveSerializer()
    departments = DepartmentSerializer(many=True, required=False)
    regions = RegionSerializer(many=True, required=False)
    projects = ProjectSerializer(many=True, required=False)
    roles = EnumField(enum_class=UserRolesChoices, required=False)
    to_all_regions = serializers.BooleanField(required=False)

    class Meta:
        model = BaseStoriesMailing
        fields = (
            'id',
            'stories',
            'publish_datetime',
            'is_published',
            'is_push',
            'departments',
            'regions',
            'projects',
            'roles',
            'to_all_regions',
            'resourcetype',
        )


class StoriesMailingUpdateSwaggerSerializer(StoriesMailingSwaggerSerializer):
    departments = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), many=True, required=False)
    regions = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(), many=True, required=False)
    projects = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), many=True, required=False)
    roles = serializers.ListField(
        child=serializers.ChoiceField(choices=UserRolesChoices),
        required=False,
    )
    to_all_regions = serializers.BooleanField(required=False)

    class Meta:
        model = BaseStoriesMailing
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
