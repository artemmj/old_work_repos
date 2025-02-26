from django.contrib.auth.models import AnonymousUser  # noqa: WPS201
from django.db.models import Exists, OuterRef, Q  # noqa: WPS347 WPS201
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from api.v1.news.filters.news import NewsFilterSet
from api.v1.news.serializers.news import (
    NewsCreateSerializer,
    NewsListIdSerializer,
    NewsRetrieveSerializer,
    NewsSerializer,
    NewsUpdateSerializer,
)
from api.v1.news.serializers.news_emoji import NewsEmojiPostSerializer
from api.v1.news.serializers.news_mobile import NewsMobileRetrieveSerializer, NewsMobileSerializer
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.serializers import EmptySerializer, EnumSerializer
from apps.helpers.viewsets import ExtendedModelViewSet, paginate_response
from apps.news.models import (
    EmojiChoices,
    News,
    NewsMailingDepartment,
    NewsMailingProject,
    NewsMailingRegion,
    NewsMailingUserRole,
    NewsRead,
)
from apps.news.services import (
    CreateOrUpdateNewsEmojiService,
    DeleteListNewsService,
    GetOrCreateNewsReadService,
    MakeTopListNewsService,
    UnmakeTopListNewsService,
)
from apps.user.permissions import IsApplicantConfirmedPermission, IsApplicantPermission, IsMasterPermission


class NewsViewSet(ExtendedModelViewSet):  # noqa: WPS214
    queryset = News.objects.non_deleted()
    serializer_class = NewsSerializer
    serializer_class_map = {
        'retrieve': NewsRetrieveSerializer,
        'create': NewsCreateSerializer,
        'partial_update': NewsUpdateSerializer,
        'news_mobile': NewsMobileSerializer,
        'news_mobile_retrieve': NewsMobileRetrieveSerializer,
        'put_emoji': NewsEmojiPostSerializer,
        'make_top_list_news': NewsListIdSerializer,
        'unmake_top_list_news': NewsListIdSerializer,
        'delete_list_news': NewsListIdSerializer,
    }
    permission_classes = (IsMasterPermission | IsApplicantPermission | IsApplicantConfirmedPermission,)
    permission_map = {
        'list': IsMasterPermission,
        'retrieve': IsMasterPermission,
        'create': IsMasterPermission,
        'partial_update': IsMasterPermission,
        'make_top_list_news': IsMasterPermission,
        'unmake_top_list_news': IsMasterPermission,
        'delete_list_news': IsMasterPermission,
    }
    search_fields = ('name',)
    filterset_class = NewsFilterSet
    ordering_fields = ('news_mailing__publish_datetime', 'is_top')
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    http_method_names = ('get', 'post', 'patch')

    def get_queryset(self):
        queryset = super().get_queryset()
        if isinstance(self.request.user, AnonymousUser):
            return queryset.none()
        if (IsApplicantPermission or IsApplicantConfirmedPermission)().has_permission(self.request, self):
            queryset = queryset.annotate(
                read_news=Exists(NewsRead.objects.filter(news=OuterRef('pk'), user=self.request.user)),
            )
            news_mailing_departments = NewsMailingDepartment.objects.filter(departments=self.request.user.department)
            news_mailing_regions = NewsMailingRegion.objects.filter(regions__in=self.request.user.regions.all())
            news_mailing_projects = NewsMailingProject.objects.filter(projects__in=self.request.user.projects.all())
            news_mailing_user_roles = NewsMailingUserRole.objects.filter(roles__contains=[self.request.user.role])
            queryset = queryset.filter(
                Q(news_mailing__in=news_mailing_departments)
                | Q(news_mailing__in=news_mailing_regions)
                | Q(news_mailing__in=news_mailing_projects)
                | Q(news_mailing__in=news_mailing_user_roles),
            ).distinct()
        return queryset.order_by('-is_top', '-created_at')

    @swagger_auto_schema(
        request_body=NewsCreateSerializer(),
        responses={
            status.HTTP_201_CREATED: NewsRetrieveSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            NewsRetrieveSerializer(instance, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @swagger_auto_schema(
        request_body=NewsUpdateSerializer(),
        responses={
            status.HTTP_200_OK: NewsRetrieveSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        instance = self.get_object()
        return Response(
            NewsRetrieveSerializer(instance, context=self.get_serializer_context()).data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_summary='Список новостей для мобилки.',
        responses={
            status.HTTP_200_OK: NewsMobileSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['get'], detail=False, url_path='news_mobile')
    def news_mobile(self, request, pk=None):
        """Список новостей для мобилки."""
        queryset = self.filter_queryset(self.get_queryset())
        return paginate_response(self, queryset)

    @swagger_auto_schema(
        operation_summary='Деталка новости для мобилки.',
        responses={
            status.HTTP_200_OK: NewsMobileRetrieveSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['get'], detail=True, url_path='news_mobile_retrieve')
    def news_mobile_retrieve(self, request, pk=None):
        """Деталка новости для мобилки."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Просмотреть новость.',
        request_body=no_body,
        responses={
            status.HTTP_200_OK: NewsMobileRetrieveSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['post'], detail=True, url_path='read_news')
    def read_news(self, request, pk=None):
        """Проcмотреть новость."""
        instance = self.get_object()

        GetOrCreateNewsReadService(news=instance, user=request.user).process()

        return Response(NewsMobileRetrieveSerializer(instance=instance, context=self.get_serializer_context()).data)

    @swagger_auto_schema(
        operation_summary='Отставить эмодзи.',
        responses={
            status.HTTP_200_OK: NewsMobileRetrieveSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['post'], detail=True)
    def put_emoji(self, request, pk=None):
        """Отставить эмодзи."""
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        CreateOrUpdateNewsEmojiService(
            news=instance,
            user=request.user,
            emoji_type=serializer.validated_data.get('emoji_type'),
        ).process()

        return Response(
            NewsMobileRetrieveSerializer(
                instance=instance,
                context=self.get_serializer_context(),
            ).data,
        )

    @swagger_auto_schema(
        operation_summary='Варианты типов эмодзи.',
        responses={
            status.HTTP_200_OK: EnumSerializer(many=True),
        },
    )
    @action(methods=['get'], detail=False, filter_backends=[])
    def emoji_type(self, request, *args, **kwargs):
        """Варианты типов эмодзи."""
        return Response(EnumSerializer(EmojiChoices, many=True).data)

    @swagger_auto_schema(
        operation_summary='Закрепить список новостей.',
        responses={
            status.HTTP_200_OK: EmptySerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['patch'], detail=False)
    def make_top_list_news(self, request, pk=None):
        """Закрепить список новостей."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        news_ids = serializer.validated_data.get('news_ids')
        MakeTopListNewsService(news_ids=news_ids).process()

        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Открепить список новостей.',
        responses={
            status.HTTP_200_OK: EmptySerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['patch'], detail=False)
    def unmake_top_list_news(self, request, pk=None):
        """Открепить список новостей."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        news_ids = serializer.validated_data.get('news_ids')
        UnmakeTopListNewsService(news_ids=news_ids).process()

        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Удалить список новостей.',
        responses={
            status.HTTP_204_NO_CONTENT: EmptySerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['post'], detail=False)
    def delete_list_news(self, request, pk=None):
        """Удалить список новостей."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        news_ids = serializer.validated_data.get('news_ids')
        DeleteListNewsService(news_ids=news_ids).process()

        return Response(status=status.HTTP_204_NO_CONTENT)
