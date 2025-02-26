from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.v1.arketa.serializers.feedback.feedback import (
    FeedbackArketaCreateSerializer,
    FeedbackArketaMobileNotificationSerializer,
)
from api.v1.arketa.serializers.feedback.notification import FeedbackArketaNotificationQuerySerializer
from apps.arketa.clients import ArketaFeedbackApiClient
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.user.permissions import IsApplicantConfirmedPermission, IsApplicantPermission, IsMasterPermission


class ArketaFeedbackViewSet(ViewSet):
    permission_classes = (IsApplicantConfirmedPermission | IsApplicantPermission | IsMasterPermission,)

    @swagger_auto_schema(
        operation_summary='Форма создания отзыва на задачу.',
        request_body=FeedbackArketaCreateSerializer(),
        responses={
            status.HTTP_201_CREATED: FeedbackArketaMobileNotificationSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        })
    def create(self, request):
        serializer = FeedbackArketaCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = request.META.get('HTTP_AUTHORIZATION')
        return Response(ArketaFeedbackApiClient(token).create(serializer.validated_data))

    @swagger_auto_schema(
        operation_summary='Экран уведомлений обратной связи.',
        query_serializer=FeedbackArketaNotificationQuerySerializer(),
        responses={
            status.HTTP_200_OK: FeedbackArketaMobileNotificationSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        })
    @action(methods=['get'], detail=False, url_path='notifications', url_name='notifications')
    def notifications(self, request):
        serializer = FeedbackArketaNotificationQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        token = request.META.get('HTTP_AUTHORIZATION')
        return Response(ArketaFeedbackApiClient(token).notifications(serializer.validated_data))

    @swagger_auto_schema(
        operation_summary='Переключатель "прочитано исполнителем".',
        responses={
            status.HTTP_200_OK: FeedbackArketaMobileNotificationSerializer(),
            status.HTTP_400_BAD_REQUEST: ErrorResponseSerializer(many=True),
        })
    @action(methods=['post'], detail=True, url_path='show_to_executor', url_name='show_to_executor')
    def show_to_executor(self, request, pk=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        return Response(ArketaFeedbackApiClient(token).show_to_executor(pk))
