from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.transaction.filters import OrganizationTransactionFilterSet
from api.v1.transaction.serializers.organization import (
    OrganizationTransactionBalanceReplenishmentSerializer,
    OrganizationTransactionCreateSerializer,
    OrganizationTransactionReadSerializer,
    OrganizationTransactionRequestSerializer,
)
from apps.helpers import exceptions
from apps.helpers.celery import CeleryResultSerializer
from apps.helpers.permissions import (
    IsAdministrator,
    IsDispatcher,
    IsOrganizationManager,
    IsOrganizationOwner,
    IsSuperUser,
)
from apps.helpers.swagger import organization_id_header
from apps.helpers.viewsets import ExtendedGenericViewSet
from apps.transaction.models import OrganizationTransaction
from apps.transaction.tasks import transactions_export_excel


class OrganizationTransactionViewSet(ExtendedGenericViewSet, mixins.ListModelMixin):
    queryset = OrganizationTransaction.objects.all()
    serializer_class = OrganizationTransactionReadSerializer
    serializer_class_map = {
        'balance_replenishment': OrganizationTransactionCreateSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
    permission_map = {
        'list': (IsOrganizationOwner | IsOrganizationManager | IsSuperUser | IsAdministrator | IsDispatcher),
        'balance_replenishment': (IsSuperUser | IsOrganizationOwner | IsOrganizationManager),
    }
    filterset_class = OrganizationTransactionFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.organization:
            return queryset
        elif (IsAdministrator | IsOrganizationOwner | IsOrganizationManager)().has_permission(self.request, self):
            return queryset.filter(organization=self.request.organization)
        return queryset

    @swagger_auto_schema(manual_parameters=[organization_id_header])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

    @swagger_auto_schema(
        request_body=OrganizationTransactionRequestSerializer,
        responses={
            status.HTTP_201_CREATED: OrganizationTransactionBalanceReplenishmentSerializer,
            status.HTTP_400_BAD_REQUEST: exceptions.BadRequestResponseSerializer,
        },
    )
    @action(methods=['post'], detail=False)
    def balance_replenishment(self, request):
        """Создание транзакции на пополнение баланса организации."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(
            OrganizationTransactionBalanceReplenishmentSerializer(instance).data,
            status=status.HTTP_201_CREATED,
        )

    @swagger_auto_schema(request_body=no_body, responses={
        status.HTTP_200_OK: CeleryResultSerializer,
        status.HTTP_400_BAD_REQUEST: exceptions.BadRequestResponseSerializer,
    })
    @action(methods=['post'], detail=False, url_path='export_excel')
    def org_transactions_export_excel(self, request):
        """Генерация отчета на транзакции организации."""
        host = f'{request.scheme}://{request.get_host()}'
        task = transactions_export_excel.delay(
            host,
            request.organization.pk if request.organization else None,
        )
        return Response({'result_id': task.id}, status=status.HTTP_200_OK)
