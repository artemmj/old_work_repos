from django.contrib.auth.models import AnonymousUser  # noqa: WPS201
from django.db.models import Exists, OuterRef, Q  # noqa: WPS347
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from api.v1.stories.filters.stories import StoriesFilterSet
from api.v1.stories.serializers.stories import (
    StoriesCreateSerializer,
    StoriesListIdSerializer,
    StoriesRetrieveSerializer,
    StoriesSerializer,
    StoriesUpdateSerializer,
    StoriesViewsReportRequestSerializer,
)
from api.v1.stories.serializers.stories_mobile import StoriesMobileSerializer
from apps.helpers.celery import CeleryResultSerializer
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.serializers import EmptySerializer
from apps.helpers.viewsets import ExtendedModelViewSet, paginate_response
from apps.stories.models import (
    Stories,
    StoriesMailingDepartment,
    StoriesMailingProject,
    StoriesMailingRegion,
    StoriesMailingUserRole,
    StoriesRead,
)
from apps.stories.services import (
    DeleteListStoriesService,
    GetOrCreateStoriesReadService,
    MakeTopListStoriesService,
    UnmakeTopListStoriesService,
)
from apps.stories.tasks import generate_stories_views_report_task
from apps.user.permissions import IsApplicantConfirmedPermission, IsApplicantPermission, IsMasterPermission


class StoriesViewSet(ExtendedModelViewSet):  # noqa: WPS214
    queryset = Stories.objects.non_deleted()
    serializer_class = StoriesSerializer
    serializer_class_map = {
        'retrieve': StoriesRetrieveSerializer,
        'create': StoriesCreateSerializer,
        'partial_update': StoriesUpdateSerializer,
        'stories_mobile': StoriesMobileSerializer,
        'read_stories': StoriesMobileSerializer,
        'delete_list_stories': StoriesListIdSerializer,
        'make_top_list_stories': StoriesListIdSerializer,
        'unmake_top_list_stories': StoriesListIdSerializer,
        'stories_views_report': StoriesViewsReportRequestSerializer,
    }
    permission_classes = (IsMasterPermission | IsApplicantPermission | IsApplicantConfirmedPermission,)
    permission_map = {
        'list': IsMasterPermission,
        'create': IsMasterPermission,
        'partial_update': IsMasterPermission,
        'retrieve': IsMasterPermission,
        'delete_list_stories': IsMasterPermission,
        'make_top_list_stories': IsMasterPermission,
        'unmake_top_list_stories': IsMasterPermission,
    }
    search_fields = ('name',)
    ordering_fields = ('stories_mailing__publish_datetime',)
    filterset_class = StoriesFilterSet
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    http_method_names = ('get', 'post', 'patch')

    def get_queryset(self):
        queryset = super().get_queryset()
        if isinstance(self.request.user, AnonymousUser):
            return queryset.none()
        if (IsApplicantPermission or IsApplicantConfirmedPermission)().has_permission(self.request, self):
            user = self.request.user
            queryset = queryset.annotate(
                read_stories=Exists(StoriesRead.objects.filter(stories=OuterRef('pk'), user=user)),
            )
            stories_mailing_departments = StoriesMailingDepartment.objects.filter(departments=user.department)
            stories_mailing_regions = StoriesMailingRegion.objects.filter(regions__in=user.regions.all())
            stories_mailing_projects = StoriesMailingProject.objects.filter(projects__in=user.projects.all())
            stories_mailing_user_roles = StoriesMailingUserRole.objects.filter(roles__contains=[user.role])
            queryset = queryset.filter(
                Q(stories_mailing__in=stories_mailing_departments)
                | Q(stories_mailing__in=stories_mailing_regions)
                | Q(stories_mailing__in=stories_mailing_projects)
                | Q(stories_mailing__in=stories_mailing_user_roles),
            ).distinct()
            return queryset.order_by('read_stories', '-is_top', '-created_at')
        return queryset.none()

    @swagger_auto_schema(
        request_body=StoriesCreateSerializer(),
        responses={
            status.HTTP_201_CREATED: StoriesRetrieveSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            StoriesRetrieveSerializer(instance, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @swagger_auto_schema(
        request_body=StoriesUpdateSerializer(),
        responses={
            status.HTTP_200_OK: StoriesRetrieveSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        instance = self.get_object()
        return Response(
            StoriesRetrieveSerializer(instance, context=self.get_serializer_context()).data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_summary='Список сторис для мобилки.',
        responses={
            status.HTTP_200_OK: StoriesMobileSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['get'], detail=False, url_path='stories_mobile')
    def stories_mobile(self, request, pk=None):
        """Список сторис для мобилки."""
        queryset = self.filter_queryset(self.get_queryset())
        return paginate_response(self, queryset)

    @swagger_auto_schema(
        operation_summary='Просмотреть сторис.',
        request_body=no_body,
        responses={
            status.HTTP_200_OK: StoriesMobileSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['post'], detail=True, url_path='read_stories')
    def read_stories(self, request, pk=None):
        """Проcмотреть сторис."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        GetOrCreateStoriesReadService(stories=instance, user=request.user).process()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Удалить список сторис.',
        responses={
            status.HTTP_204_NO_CONTENT: EmptySerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['post'], detail=False, url_path='delete_list_stories')
    def delete_list_stories(self, request, pk=None):
        """Удалить список сторис."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stories_ids = serializer.validated_data.get('stories_ids')
        DeleteListStoriesService(stories_ids=stories_ids).process()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_summary='Отчет по просмотрам сторис.',
        request_body=StoriesViewsReportRequestSerializer(),
        responses={
            status.HTTP_200_OK: CeleryResultSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['POST'], detail=False)
    def stories_views_report(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = generate_stories_views_report_task.delay(serializer.data.get('start'), serializer.data.get('end'))
        return Response({'result_id': task.id})

    @swagger_auto_schema(
        operation_summary='Закрепить список сторис.',
        responses={
            status.HTTP_200_OK: EmptySerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['patch'], detail=False)
    def make_top_list_stories(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stories_ids = serializer.validated_data.get('stories_ids')
        MakeTopListStoriesService(stories_ids=stories_ids).process()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Открепить список сторис.',
        responses={
            status.HTTP_200_OK: EmptySerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['patch'], detail=False)
    def unmake_top_list_stories(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stories_ids = serializer.validated_data.get('stories_ids')
        UnmakeTopListStoriesService(stories_ids=stories_ids).process()
        return Response(status=status.HTTP_200_OK)
