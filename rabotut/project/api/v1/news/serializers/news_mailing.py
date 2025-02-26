from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_polymorphic.serializers import PolymorphicSerializer

from api.v1.departaments.serializers import DepartmentSerializer
from api.v1.news.serializers.news import NewsRetrieveSerializer, NewsSerializer
from api.v1.projects.serializers import ProjectSerializer
from api.v1.regions.serializers import RegionSerializer
from apps.departments.models import Department
from apps.helpers.serializers import EnumField, EnumSerializer
from apps.news.models import (
    BaseNewsMailing,
    NewsMailingDepartment,
    NewsMailingProject,
    NewsMailingRegion,
    NewsMailingUserRole,
    UserRolesChoices,
)
from apps.projects.models import Project
from apps.regions.models import Region


class BaseNewsMailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseNewsMailing
        fields = ('id', 'news', 'publish_datetime', 'is_published', 'is_push')
        read_only_fields = ('id',)


class BaseNewsMailingListSerializer(BaseNewsMailingSerializer):
    news = NewsSerializer()

    class Meta:
        model = BaseNewsMailing
        fields = ('id', 'news', 'publish_datetime', 'is_published', 'is_push')


class NewsMailingDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsMailingDepartment
        fields = ('id', 'news', 'departments', 'publish_datetime', 'is_published', 'is_push')
        read_only_fields = ('id',)


class NewsMailingDepartmentRetrieveSerializer(serializers.ModelSerializer):
    news = NewsRetrieveSerializer()
    departments = DepartmentSerializer(many=True)

    class Meta:
        model = NewsMailingDepartment
        fields = ('id', 'news', 'departments', 'publish_datetime', 'is_published', 'is_push')


class NewsMailingRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsMailingRegion
        fields = ('id', 'news', 'regions', 'publish_datetime', 'is_published', 'is_push', 'to_all_regions')
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


class NewsMailingRegionRetrieveSerializer(serializers.ModelSerializer):
    news = NewsRetrieveSerializer()
    regions = RegionSerializer(many=True)

    class Meta:
        model = NewsMailingRegion
        fields = ('id', 'news', 'regions', 'publish_datetime', 'is_published', 'is_push', 'to_all_regions')
        read_only_fields = ('id',)


class NewsMailingProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsMailingProject
        fields = ('id', 'news', 'projects', 'publish_datetime', 'is_published', 'is_push')
        read_only_fields = ('id',)


class NewsMailingProjectRetrieveSerializer(serializers.ModelSerializer):
    news = NewsRetrieveSerializer()
    projects = ProjectSerializer(many=True)

    class Meta:
        model = NewsMailingProject
        fields = ('id', 'news', 'projects', 'publish_datetime', 'is_published', 'is_push')
        read_only_fields = ('id',)


class NewsMailingUserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsMailingUserRole
        fields = ('id', 'news', 'roles', 'publish_datetime', 'is_published', 'is_push')
        read_only_fields = ('id',)


class NewsMailingUserRoleRetrieveSerializer(serializers.ModelSerializer):
    news = NewsRetrieveSerializer()
    roles = serializers.SerializerMethodField()

    class Meta:
        model = NewsMailingUserRole
        fields = ('id', 'news', 'roles', 'publish_datetime', 'is_published', 'is_push')
        read_only_fields = ('id',)

    @swagger_serializer_method(serializer_or_field=EnumSerializer(many=True))
    def get_roles(self, obj):  # noqa: WPS110
        roles = [UserRolesChoices[role.upper()] for role in obj.roles]
        return EnumSerializer(roles, many=True).data


class NewsMailingPolymorphicSerializer(PolymorphicSerializer):
    base_serializer_class = BaseNewsMailingSerializer
    model_serializer_mapping = {
        NewsMailingDepartment: NewsMailingDepartmentSerializer,
        NewsMailingRegion: NewsMailingRegionSerializer,
        NewsMailingProject: NewsMailingProjectSerializer,
        NewsMailingUserRole: NewsMailingUserRoleSerializer,
    }

    def update(self, instance, validated_data):
        if instance.is_published:
            raise ValidationError('Новость уже опубликована.')
        return super().update(instance, validated_data)


class NewsMailingRetrievePolymorphicSerializer(PolymorphicSerializer):
    base_serializer_class = BaseNewsMailingSerializer
    model_serializer_mapping = {
        NewsMailingDepartment: NewsMailingDepartmentRetrieveSerializer,
        NewsMailingRegion: NewsMailingRegionRetrieveSerializer,
        NewsMailingProject: NewsMailingProjectRetrieveSerializer,
        NewsMailingUserRole: NewsMailingUserRoleRetrieveSerializer,
    }


class NewsMailingSwaggerSerializer(serializers.ModelSerializer):
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
            'NewsMailingDepartment',
            'NewsMailingRegion',
            'NewsMailingProject',
            'NewsMailingUserRole',
        ),
        required=True,
    )

    class Meta:
        model = BaseNewsMailing
        fields = (
            'id',
            'news',
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


class NewsMailingRetrieveSwaggerSerializer(NewsMailingSwaggerSerializer):
    news = NewsRetrieveSerializer()
    departments = DepartmentSerializer(many=True, required=False)
    regions = RegionSerializer(many=True, required=False)
    projects = ProjectSerializer(many=True, required=False)
    roles = EnumField(enum_class=UserRolesChoices, required=False)
    to_all_regions = serializers.BooleanField(required=False)

    class Meta:
        model = BaseNewsMailing
        fields = (
            'id',
            'news',
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


class NewsMailingUpdateSwaggerSerializer(NewsMailingSwaggerSerializer):
    departments = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), many=True, required=False)
    regions = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(), many=True, required=False)
    projects = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), many=True, required=False)
    roles = serializers.ListField(
        child=serializers.ChoiceField(choices=UserRolesChoices),
        required=False,
    )
    to_all_regions = serializers.BooleanField(required=False)

    class Meta:
        model = BaseNewsMailing
        fields = (
            'id',
            'publish_datetime',
            'is_published',
            'is_push',
            'departments',
            'regions',
            'projects',
            'roles',
            'to_all_regions',
        )
