from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.template.serializers.invitation import (
    TemplateInvitationCreateByOrganizationSerializer,
    TemplateInvitationCreateByPhoneSerializer,
    TemplateInvitationReadSerializer,
)
from apps.helpers.celery import CeleryResultSerializer
from apps.helpers.exceptions import BadRequestResponseSerializer
from apps.helpers.permissions import IsAdministrator, IsDispatcher
from apps.helpers.viewsets import ReadExtendedModelViewSet
from apps.template.models import TemplateInvitation, TemplateInvitationStatuses
from apps.template.tasks import create_template_invitation_task


class TemplateInvitationViewSet(ReadExtendedModelViewSet):
    queryset = TemplateInvitation.objects.all()
    serializer_class = TemplateInvitationReadSerializer
    serializer_class_map = {
        'create_by_phone': TemplateInvitationCreateByPhoneSerializer,
        'create_by_organization': TemplateInvitationCreateByOrganizationSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = super().get_queryset()
        if (IsAdministrator | IsDispatcher)().has_permission(self.request, self):
            return queryset
        return queryset.filter(user=self.request.user, status=TemplateInvitationStatuses.PENDING)

    @swagger_auto_schema(
        request_body=TemplateInvitationCreateByPhoneSerializer,
        responses={
            status.HTTP_200_OK: TemplateInvitationReadSerializer,
            status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
            status.HTTP_404_NOT_FOUND: BadRequestResponseSerializer,
        },
    )
    @action(methods=['post'], detail=False)
    def create_by_phone(self, request):
        """Создать приглашение для пользователя."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(
            TemplateInvitationReadSerializer(instance, context=self.get_serializer_context()).data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        request_body=TemplateInvitationCreateByOrganizationSerializer,
        responses={
            status.HTTP_200_OK: CeleryResultSerializer,
            status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
            status.HTTP_404_NOT_FOUND: BadRequestResponseSerializer,
        },
    )
    @action(methods=['post'], detail=False)
    def create_by_organization(self, request):
        """Создать приглашения для участников организации."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization_id = str(serializer.validated_data['organization'].id)
        template_id = str(serializer.validated_data['template'].id)
        owner_id = str(request.user.id)
        task = create_template_invitation_task.delay(organization_id, template_id, owner_id)
        return Response(CeleryResultSerializer({'result_id': task.id}).data, status=status.HTTP_200_OK)

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
        instance.status = TemplateInvitationStatuses.ACCEPTED
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
        instance.status = TemplateInvitationStatuses.CANCELED
        instance.save()
        return Response(status=status.HTTP_200_OK)
