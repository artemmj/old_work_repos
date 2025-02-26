from constance import config
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.v1.organization.filters.membership import MembershipFilterSet
from api.v1.organization.serializers.membership import (
    MembershipReadSerializer,
    MembershipUpdateSerializer,
    MembershipWriteSerializer,
)
from api.v1.organization.serializers.organization import MembershipsOrganizationQuerySerializer
from apps.helpers.exceptions import BadRequestResponseSerializer
from apps.helpers.permissions import (
    IsAdministrator,
    IsDispatcher,
    IsOrganizationManager,
    IsOrganizationOwner,
    IsSuperUser,
)
from apps.helpers.serializers import EnumSerializer
from apps.helpers.viewsets import CRUDExtendedModelViewSet, paginate_response
from apps.organization.models.membership import Membership, MembershipRoleChoices

uuid = '[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}'


class MembershipViewSet(CRUDExtendedModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipReadSerializer
    serializer_class_map = {
        'create': MembershipWriteSerializer,
        'update': MembershipUpdateSerializer,
        'partial_update': MembershipUpdateSerializer,
    }
    filterset_class = MembershipFilterSet
    search_fields = (
        'user__last_name',
        'user__phone',
        'user__roles',
    )
    ordering_fields = (
        'user__last_name',
        'user__phone',
        'user__roles',
    )
    permission_classes = (permissions.IsAuthenticated,)
    permission_map = {
        'create': (IsSuperUser | IsAdministrator | IsDispatcher),
        'update': (IsSuperUser | IsAdministrator | IsDispatcher),
        'partial_update': (IsSuperUser | IsAdministrator | IsDispatcher),
        'delete': (
            IsSuperUser | IsAdministrator | IsDispatcher | IsOrganizationOwner | IsOrganizationManager
        ),
    }

    @swagger_auto_schema(
        query_serializer=MembershipsOrganizationQuerySerializer,
        responses={
            status.HTTP_200_OK: MembershipReadSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
        },
    )
    def list(self, request):
        """Список участников организации."""
        qs = self.filter_queryset(self.get_queryset().select_related('user'))
        if 'only_inspectors' in request.query_params and request.query_params.get('only_inspectors') == 'true':
            qs = qs.filter(role=MembershipRoleChoices.INSPECTOR)
        return paginate_response(self, qs, MembershipReadSerializer, context=self.get_serializer_context())

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, serializer.validated_data)
        return Response(MembershipReadSerializer(instance).data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Исключить из организации."""  # noqa: DAR401c
        instance = self.get_object()
        qs = self.queryset.filter(user=request.user)
        is_active = instance.is_active
        if qs.count() == 1:
            raise ValidationError({'error': config.ORG_MEMBERSHIP_CANT_LEAVE_LAST_ORG_ERROR})
        self.perform_destroy(instance)
        if is_active:
            instance = qs.first()
            instance.is_active = True
            instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(request_body=MembershipWriteSerializer, responses={201: MembershipReadSerializer})
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(MembershipReadSerializer(instance).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumSerializer(many=True)})
    @action(methods=['get'], detail=False, url_path='roles')
    def roles(self, request):
        """Возвращает возможные роли участников организаций."""
        return Response(EnumSerializer(MembershipRoleChoices, many=True).data)
