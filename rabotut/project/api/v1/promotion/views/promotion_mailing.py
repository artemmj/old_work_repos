from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from api.v1.promotion.serializers import (
    BasePromotionMailingListSerializer,
    PromotionMailingPolymorphicSerializer,
    PromotionMailingRetrievePolymorphicSerializer,
    PromotionMailingRetrieveSwaggerSerializer,
    PromotionMailingSwaggerSerializer,
    PromotionMailingUpdateSwaggerSerializer,
)
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.viewsets import ExtendedModelViewSet
from apps.promotion.models import BasePromotionMailing
from apps.user.permissions import IsMasterPermission


class PromotionMailingViewSet(ExtendedModelViewSet):
    queryset = BasePromotionMailing.objects.filter(
        promotion__deleted_at__isnull=True,
    ).order_by('-promotion__is_top', '-created_at')
    serializer_class = PromotionMailingPolymorphicSerializer
    serializer_class_map = {
        'list': BasePromotionMailingListSerializer,
        'retrieve': PromotionMailingRetrievePolymorphicSerializer,
    }
    permission_classes = (IsMasterPermission,)
    ordering_fields = (
        'publish_datetime',
        'promotion__is_top',
        'promotion__is_main_display',
        'promotion__is_hidden',
        'type',
    )
    filter_backends = (OrderingFilter, SearchFilter)
    http_method_names = ('get', 'post', 'patch')

    @swagger_auto_schema(
        request_body=no_body,
        responses={
            status.HTTP_200_OK: PromotionMailingRetrieveSwaggerSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=PromotionMailingSwaggerSerializer(),
        responses={
            status.HTTP_201_CREATED: PromotionMailingRetrieveSwaggerSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            PromotionMailingRetrievePolymorphicSerializer(instance).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @swagger_auto_schema(
        request_body=PromotionMailingUpdateSwaggerSerializer(),
        responses={
            status.HTTP_200_OK: PromotionMailingRetrieveSwaggerSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        instance = self.get_object()
        return Response(PromotionMailingRetrievePolymorphicSerializer(instance).data, status=status.HTTP_200_OK)
