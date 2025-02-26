from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.organization.filters.invitation import OrgInvitationFilterSet
from api.v1.organization.serializers.invitation import OrgInvitationReadSerializer, OrgInvitationWriteSerializer
from apps.helpers.exceptions import BadRequestResponseSerializer
from apps.helpers.viewsets import CRDExtendedModelViewSet
from apps.organization.models import OrgInvitation
from apps.organization.services import SendNotificationOrgInvitationService


class OrgInvitationViewSet(CRDExtendedModelViewSet):
    queryset = OrgInvitation.objects.exclude(is_accepted=True)
    serializer_class = OrgInvitationReadSerializer
    serializer_class_map = {
        'create': OrgInvitationWriteSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
    filterset_class = OrgInvitationFilterSet

    @swagger_auto_schema(
        request_body=no_body,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
        },
    )
    @action(methods=['post'], detail=True)
    def accept(self, request, pk=None):
        """Принять приглашение."""
        instance = self.get_object()
        instance.is_accepted = True
        instance.save()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=no_body,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
        },
    )
    @action(methods=['post'], detail=True)
    def reject(self, request, pk=None):
        """Отклонить приглашение."""
        instance = self.get_object()
        instance.is_accepted = False
        instance.save()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=no_body,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
        },
    )
    @action(methods=['patch'], detail=True)
    def restore(self, request, pk=None):
        """Восстановить отклоненное приглашение."""
        instance = self.get_object()
        if instance.is_accepted is False:
            instance.is_accepted = None
            instance.save()
            SendNotificationOrgInvitationService().process(instance)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=no_body,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
        },
    )
    @action(methods=['post'], detail=True)
    def send_notification(self, request, pk=None):
        """Отправка оповещения пользователю о приглашении."""
        instance = self.get_object()
        if instance.is_accepted is None:
            SendNotificationOrgInvitationService().process(instance)
        return Response(status=status.HTTP_200_OK)
