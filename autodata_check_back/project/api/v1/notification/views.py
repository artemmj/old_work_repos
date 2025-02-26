from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.notification.filters import NotificationFilterSet
from api.v1.notification.serializers import (
    NotificationNewCountSerializer,
    NotificationPolymorphicSerializer,
    NotificationResponseSwaggerSerializer,
    NotificationViewedSerializer,
    SendOrgBalanceEmailSerializer,
)
from api.v1.notification.services import send_org_balance_email_celery_wrapper
from apps.helpers.exceptions import BadRequestResponseSerializer
from apps.helpers.serializers import EmptySerializer
from apps.helpers.viewsets import ReadExtendedModelViewSet, paginate_response
from apps.notification.models import BaseNotification, NotificationStatuses


class NotificationViewSet(ReadExtendedModelViewSet):
    queryset = BaseNotification.objects.all()
    serializer_class = NotificationPolymorphicSerializer
    serializer_class_map = {
        'viewed': NotificationViewedSerializer,
        'new_count': NotificationNewCountSerializer,
    }
    permission_classes = (IsAuthenticated,)
    filterset_class = NotificationFilterSet
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: NotificationResponseSwaggerSerializer(many=True),
        status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
    })
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: NotificationResponseSwaggerSerializer(many=True),
        status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
    })
    @action(methods=['get'], detail=False)
    def list_new(self, request, *args, **kwargs):
        """Получить только новые уведомления."""
        return paginate_response(
            self,
            self.get_queryset().filter(status=NotificationStatuses.NEW),
            NotificationPolymorphicSerializer,
        )

    @swagger_auto_schema(
        request_body=NotificationViewedSerializer,
        responses={
            status.HTTP_200_OK: EmptySerializer,
            status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
            status.HTTP_404_NOT_FOUND: BadRequestResponseSerializer,
        },
    )
    @action(methods=['patch'], detail=False)
    def viewed(self, request):
        """Просмотреть уведомления."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        notifications = serializer.data['notifications']
        BaseNotification.objects.filter(
            id__in=notifications,
        ).update(status=NotificationStatuses.VIEWED)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: NotificationNewCountSerializer})
    @action(methods=['get'], detail=False)
    def new_count(self, request):
        """Кол-во новых уведомлений."""
        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.filter(status=NotificationStatuses.NEW).count()
        serializer = self.get_serializer({'new_count': count})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=EmptySerializer, responses={status.HTTP_200_OK: EmptySerializer})
    @action(methods=['post'], detail=False)
    def read_all(self, request):
        """Прочитать все уведомления."""
        notifications = self.get_queryset().filter(status=NotificationStatuses.NEW)
        notifications.update(status=NotificationStatuses.VIEWED)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=SendOrgBalanceEmailSerializer, responses={status.HTTP_200_OK: EmptySerializer})
    @action(methods=['post'], detail=False)
    def send_org_balance_email(self, request):
        serializer = SendOrgBalanceEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_org_balance_email_celery_wrapper.delay(serializer.data, request.user.pk)
        return Response(status=status.HTTP_200_OK)
