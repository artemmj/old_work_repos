from django.contrib.auth.models import AnonymousUser  # noqa: WPS201
from django.db.models import Exists, OuterRef, Q  # noqa: WPS347
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.serializers import EmptySerializer, EnumSerializer
from apps.helpers.viewsets import ExtendedModelViewSet, paginate_response
from apps.promotion.models import (
    EmojiChoices,
    Promotion,
    PromotionMailingDepartment,
    PromotionMailingProject,
    PromotionMailingRegion,
    PromotionMailingUserRole,
    PromotionRead,
)
from apps.promotion.services import (
    CreateOrUpdatePromotionEmojiService,
    DeleteListPromotionService,
    GetOrCreatePromotionRead,
    MakeHiddenListPromotionService,
    MakeTopListPromotionService,
    UnmakeTopListPromotionService,
)
from apps.user.permissions import IsApplicantConfirmedPermission, IsApplicantPermission, IsMasterPermission

from ..filters import PromotionFilter
from ..serializers import (
    PromotionCreateSerializer,
    PromotionEmojiPostSerializer,
    PromotionListIdSerializer,
    PromotionMobileRetrieveSerializer,
    PromotionMobileSerializer,
    PromotionRetrieveSerializer,
    PromotionSerializer,
    PromotionUpdateSerializer,
)


class PromotionViewSet(ExtendedModelViewSet):  # noqa: WPS214
    queryset = Promotion.objects.non_deleted()
    serializer_class = PromotionSerializer
    serializer_class_map = {
        'retrieve': PromotionRetrieveSerializer,
        'create': PromotionCreateSerializer,
        'partial_update': PromotionUpdateSerializer,
        'promotions_mobile': PromotionMobileSerializer,
        'promotions_mobile_retrieve': PromotionMobileRetrieveSerializer,
        'put_emoji': PromotionEmojiPostSerializer,
        'make_top_list_promotions': PromotionListIdSerializer,
        'unmake_top_list_promotions': PromotionListIdSerializer,
        'delete_list_promotions': PromotionListIdSerializer,
        'make_hidden_list_promotions': PromotionListIdSerializer,
    }
    permission_classes = (IsMasterPermission | IsApplicantPermission | IsApplicantConfirmedPermission,)
    permission_map = {
        'list': IsMasterPermission,
        'retrieve': IsMasterPermission,
        'create': IsMasterPermission,
        'partial_update': IsMasterPermission,
        'make_top_list_promotions': IsMasterPermission,
        'unmake_top_list_promotions': IsMasterPermission,
        'delete_list_promotions': IsMasterPermission,
        'make_hidden_list_promotions': IsMasterPermission,
    }
    filterset_class = PromotionFilter
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    ordering_fields = ('mailings__publish_datetime', 'is_top', 'is_main_display', 'is_hidden')
    http_method_names = ('get', 'post', 'patch')

    def get_queryset(self):
        queryset = super().get_queryset()
        if isinstance(self.request.user, AnonymousUser):
            return queryset.none()
        if (IsApplicantPermission or IsApplicantConfirmedPermission)().has_permission(self.request, self):
            queryset = queryset.annotate(
                read_promotions=Exists(PromotionRead.objects.filter(promotion=OuterRef('pk'), user=self.request.user)),
            )
            mailing_departments = PromotionMailingDepartment.objects.filter(departments=self.request.user.department)
            mailing_regions = PromotionMailingRegion.objects.filter(regions__in=self.request.user.regions.all())
            mailing_projects = PromotionMailingProject.objects.filter(projects__in=self.request.user.projects.all())
            mailing_user_roles = PromotionMailingUserRole.objects.filter(roles__contains=[self.request.user.role])
            queryset = queryset.filter(
                Q(mailings__in=mailing_departments)
                | Q(mailings__in=mailing_regions)
                | Q(mailings__in=mailing_projects)
                | Q(mailings__in=mailing_user_roles),
            ).distinct()
        return queryset.order_by('-is_top', '-created_at')

    @swagger_auto_schema(
        request_body=PromotionCreateSerializer(),
        responses={
            status.HTTP_201_CREATED: PromotionRetrieveSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(PromotionRetrieveSerializer(instance).data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        request_body=PromotionUpdateSerializer(),
        responses={
            status.HTTP_200_OK: PromotionRetrieveSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        instance = self.get_object()
        return Response(PromotionRetrieveSerializer(instance).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Список акций для мобилки.',
        responses={
            status.HTTP_200_OK: PromotionMobileSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['get'], detail=False, url_path='promotions_mobile')
    def promotions_mobile(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.exclude(end_date__lte=timezone.now())
        return paginate_response(self, queryset)

    @swagger_auto_schema(
        operation_summary='Деталка акции для мобилки.',
        responses={
            status.HTTP_200_OK: PromotionMobileRetrieveSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['get'], detail=True, url_path='promotions_mobile_retrieve')
    def promotions_mobile_retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Просмотреть акцию.',
        request_body=no_body,
        responses={
            status.HTTP_200_OK: PromotionMobileRetrieveSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['post'], detail=True, url_path='read_promotion')
    def read_promotion(self, request, pk=None):
        instance = self.get_object()
        GetOrCreatePromotionRead(promotion=instance, user=request.user).process()
        return Response(
            PromotionMobileRetrieveSerializer(instance=instance, context=self.get_serializer_context()).data,
        )

    @swagger_auto_schema(
        operation_summary='Отставить эмодзи.',
        responses={
            status.HTTP_200_OK: PromotionMobileRetrieveSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['post'], detail=True)
    def put_emoji(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        CreateOrUpdatePromotionEmojiService(
            promotion=instance,
            user=request.user,
            emoji_type=serializer.validated_data.get('emoji_type'),
        ).process()
        return Response(
            PromotionMobileRetrieveSerializer(instance=instance, context=self.get_serializer_context()).data,
        )

    @swagger_auto_schema(
        operation_summary='Варианты типов эмодзи.',
        responses={
            status.HTTP_200_OK: EnumSerializer(many=True),
        },
    )
    @action(methods=['get'], detail=False, filter_backends=[])
    def emoji_type(self, request, *args, **kwargs):
        return Response(EnumSerializer(EmojiChoices, many=True).data)

    @swagger_auto_schema(
        operation_summary='Закрепить список акций.',
        responses={
            status.HTTP_200_OK: EmptySerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['patch'], detail=False)
    def make_top_list_promotions(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        promotions_ids = serializer.validated_data.get('promotion_ids')
        MakeTopListPromotionService(promotions_ids=promotions_ids).process()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Открепить список акций.',
        responses={
            status.HTTP_200_OK: EmptySerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['patch'], detail=False)
    def unmake_top_list_promotions(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        promotions_ids = serializer.validated_data.get('promotion_ids')
        UnmakeTopListPromotionService(promotions_ids=promotions_ids).process()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Удалить список акций.',
        responses={
            status.HTTP_204_NO_CONTENT: EmptySerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['post'], detail=False)
    def delete_list_promotions(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        promotions_ids = serializer.validated_data.get('promotion_ids')
        DeleteListPromotionService(promotions_ids=promotions_ids).process()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_summary='Скрыть список акций.',
        responses={
            status.HTTP_204_NO_CONTENT: EmptySerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    @action(methods=['post'], detail=False)
    def make_hidden_list_promotions(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        promotions_ids = serializer.validated_data.get('promotion_ids')
        MakeHiddenListPromotionService(promotions_ids=promotions_ids).process()
        return Response(status=status.HTTP_204_NO_CONTENT)
