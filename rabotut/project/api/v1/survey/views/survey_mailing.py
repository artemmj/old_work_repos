from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.viewsets import ExtendedModelViewSet
from apps.survey.models import BaseSurveyMailing
from apps.user.permissions import IsMasterPermission

from ..serializers import (
    BaseSurveyMailingListSerializer,
    SurveyMailingPolymorphicSerializer,
    SurveyMailingRetrievePolymorphicSerializer,
    SurveyMailingRetrieveSwaggerSerializer,
    SurveyMailingSwaggerSerializer,
    SurveyMailingUpdateSwaggerSerializer,
)


class SurveyMailingViewSet(ExtendedModelViewSet):
    queryset = BaseSurveyMailing.objects.filter(
        survey__deleted_at__isnull=True,
    ).order_by('-created_at')
    serializer_class = SurveyMailingPolymorphicSerializer
    serializer_class_map = {
        'list': BaseSurveyMailingListSerializer,
        'retrieve': SurveyMailingRetrievePolymorphicSerializer,
    }
    permission_classes = (IsMasterPermission,)
    ordering_fields = ('publish_datetime', 'survey__is_self_option', 'type')
    filter_backends = (OrderingFilter, SearchFilter)
    http_method_names = ('get', 'post', 'patch')

    @swagger_auto_schema(
        request_body=no_body,
        responses={
            status.HTTP_200_OK: SurveyMailingSwaggerSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=no_body,
        responses={
            status.HTTP_200_OK: SurveyMailingRetrieveSwaggerSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=SurveyMailingSwaggerSerializer(),
        responses={
            status.HTTP_201_CREATED: SurveyMailingRetrieveSwaggerSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            SurveyMailingRetrievePolymorphicSerializer(instance).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @swagger_auto_schema(
        request_body=SurveyMailingUpdateSwaggerSerializer(),
        responses={
            status.HTTP_200_OK: SurveyMailingRetrieveSwaggerSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        instance = self.get_object()
        return Response(SurveyMailingRetrievePolymorphicSerializer(instance).data, status=status.HTTP_200_OK)
