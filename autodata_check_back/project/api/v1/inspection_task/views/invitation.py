from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.inspection_task.serializers.invitation import InvitationReadSerializer
from apps.helpers.exceptions import BadRequestResponseSerializer
from apps.helpers.viewsets import ReadExtendedModelViewSet
from apps.inspection_task.models.invitation import Invitation


class InvitationViewSet(ReadExtendedModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationReadSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(inspector=self.request.user, is_accepted__isnull=True)

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
