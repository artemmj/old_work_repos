from decimal import Decimal

from constance import config
from django.db.models import Count, Q  # noqa: WPS347
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.v1.organization.serializers import (  # noqa: WPS235
    OrganizationAdminCompactQuerySerializer,
    OrganizationAdminCompactSerializer,
    OrganizationCreateForUserRequestSerializer,
    OrganizationCreateForUserSerializer,
    OrganizationInfoSerializer,
    OrganizationOnlyINNWriteSerializer,
    OrganizationReadSerializer,
    OrganizationUpdateSelfInspectionPriceSerializer,
    OrganizationWriteSerializer,
)
from api.v1.organization.serializers.organization import (
    ActivateSubscriptionSerializer,
    OrganizationChangeBalanceSerializer,
)
from apps.dadata.services import DadataFindByINNService
from apps.helpers import exceptions
from apps.helpers.celery import CeleryResultSerializer
from apps.helpers.permissions import (
    IsAdministrator,
    IsCustomer,
    IsDispatcher,
    IsOrganizationManager,
    IsOrganizationOwner,
    IsSuperUser,
)
from apps.helpers.serializers import EmptySerializer
from apps.helpers.swagger import organization_id_header
from apps.helpers.viewsets import ExtendedModelViewSet, paginate_response
from apps.inspection.models.inspection import StatusChoices
from apps.inspection_task.models.task import InspectorTaskStatuses
from apps.organization.models import Organization
from apps.organization.models.membership import MembershipRoleChoices
from apps.organization.tasks import organizations_export_excel_task
from apps.tariffs.services.activate import ActivateSubscriptionService
from apps.transaction.models.abstract import TransactionTypes
from apps.transaction.models.organization import OrganizationTransaction, OrganizationTransactionOperations


class OrganizationViewSet(ExtendedModelViewSet):  # noqa: WPS214
    queryset = Organization.objects.all()
    serializer_class = OrganizationReadSerializer
    serializer_class_map = {
        'create': OrganizationOnlyINNWriteSerializer,
        'update': OrganizationWriteSerializer,
        'partial_update': OrganizationWriteSerializer,
        'update_self_inspection_price': OrganizationUpdateSelfInspectionPriceSerializer,
        'admin_compact': OrganizationAdminCompactSerializer,
        'admin_create_organization_for_user': OrganizationCreateForUserSerializer,
        'activate_subscription': ActivateSubscriptionSerializer,
        'find_organization_by_inn': OrganizationOnlyINNWriteSerializer,
        'add_balance': OrganizationChangeBalanceSerializer,
        'withdraw_balance': OrganizationChangeBalanceSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
    permission_map = {
        'create': (IsCustomer | IsSuperUser | IsAdministrator | IsDispatcher),
        'update': (IsOrganizationOwner | IsSuperUser | IsAdministrator | IsDispatcher),
        'partial_update': (IsOrganizationOwner | IsSuperUser | IsAdministrator | IsDispatcher),
        'destroy': (IsSuperUser | IsDispatcher | IsAdministrator),
        'update_self_inspection_price': (IsSuperUser | IsAdministrator | IsDispatcher),
        'admin_compact': (IsSuperUser | IsAdministrator | IsDispatcher),
        'admin_create_organization_for_user': (IsSuperUser | IsAdministrator | IsDispatcher),
        'activate_subscription': (IsAdministrator | IsDispatcher | IsOrganizationOwner | IsOrganizationManager),
        'deactivate_subscription': (IsAdministrator | IsDispatcher | IsOrganizationOwner | IsOrganizationManager),
    }
    search_fields = (
        'title',
        'inn',
        'self_inspection_price',
        'num_inspections',
    )
    ordering_fields = (
        'title',
        'inn',
        'num_memberships',
        'self_inspection_price',
        'num_inspections',
        'tariffs',
        'balance',
    )

    def get_queryset(self):
        queryset = Organization.objects.annotate(
            num_inspections=Count('inspections', filter=Q(inspections__status=StatusChoices.COMPLETE)),
        )
        if (IsSuperUser | IsAdministrator | IsDispatcher)().has_permission(self.request, self):
            return queryset
        return queryset.filter(users=self.request.user)

    @swagger_auto_schema(
        request_body=OrganizationOnlyINNWriteSerializer,
        responses={
            status.HTTP_201_CREATED: OrganizationReadSerializer,
            status.HTTP_400_BAD_REQUEST: exceptions.BadRequestResponseSerializer,
        },
    )
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            OrganizationReadSerializer(instance=serializer.instance, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED,
        )

    @swagger_auto_schema(
        request_body=OrganizationUpdateSelfInspectionPriceSerializer,
        responses={
            status.HTTP_200_OK: OrganizationReadSerializer,
            status.HTTP_400_BAD_REQUEST: exceptions.BadRequestResponseSerializer,
        },
    )
    @action(methods=['patch'], detail=True)
    def update_self_inspection_price(self, request, pk=None):
        """Изменение цены за самостоятельный осмотр у организации."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            OrganizationReadSerializer(instance=instance, context=self.get_serializer_context()).data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        request_body=OrganizationChangeBalanceSerializer,
        responses={
            status.HTTP_200_OK: OrganizationReadSerializer,
            status.HTTP_400_BAD_REQUEST: exceptions.BadRequestResponseSerializer,
        },
    )
    @action(methods=['post'], detail=True)
    def add_balance(self, request, pk=None):
        """Ручное пополнение баланса."""
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        OrganizationTransaction.objects.create(
            organization=instance,
            user=request.user,
            type=TransactionTypes.ADD,
            operation=OrganizationTransactionOperations.HAND_BALANCE_REPLENISHMENT,
            amount=Decimal(serializer.data.get('value')),
        )
        instance.refresh_from_db()
        return Response(
            OrganizationReadSerializer(instance=instance, context=self.get_serializer_context()).data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        request_body=OrganizationChangeBalanceSerializer,
        responses={
            status.HTTP_200_OK: OrganizationReadSerializer,
            status.HTTP_400_BAD_REQUEST: exceptions.BadRequestResponseSerializer,
        },
    )
    @action(methods=['post'], detail=True)
    def withdraw_balance(self, request, pk=None):
        """Ручное списание с баланса."""
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        OrganizationTransaction.objects.create(
            organization=instance,
            user=request.user,
            type=TransactionTypes.WITHDRAW,
            operation=OrganizationTransactionOperations.HAND_BALANCE_WITHDRAW,
            amount=Decimal(serializer.data.get('value')),
        )
        instance.refresh_from_db()
        return Response(
            OrganizationReadSerializer(instance=instance, context=self.get_serializer_context()).data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        query_serializer=OrganizationAdminCompactQuerySerializer,
        responses={
            status.HTTP_200_OK: OrganizationAdminCompactSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: exceptions.BadRequestResponseSerializer,
        },
    )
    @action(methods=['get'], detail=False, url_path='admin/compact')
    def admin_compact(self, request):  # noqa: WPS210
        """Список организаций с урезанными данными для админки."""
        query_serializer = OrganizationAdminCompactQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        query_user = query_serializer.validated_data['user']
        query_membership_role = query_serializer.validated_data.get('membership_role')
        filters = {'users': query_user}
        if query_membership_role:
            filters['membership__role'] = query_membership_role
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(**filters).annotate(
            num_tasks=Count(
                'inspection_tasks',
                filter=~Q(inspection_tasks__status=InspectorTaskStatuses.DRAFT),
            ),
        )
        context = self.get_serializer_context()
        context['query_user'] = query_user
        return paginate_response(self, queryset, context=context)

    @swagger_auto_schema(
        request_body=OrganizationCreateForUserRequestSerializer,
        responses={
            status.HTTP_201_CREATED: OrganizationCreateForUserSerializer,
            status.HTTP_400_BAD_REQUEST: exceptions.BadRequestResponseSerializer,
        },
    )
    @action(methods=['post'], detail=False, url_path='admin/create')
    def admin_create_organization_for_user(self, request):
        """Создание организации определенному пользователю из админки."""
        request_serializer = OrganizationCreateForUserRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        req_user = request_serializer.validated_data.pop('user')
        context = self.get_serializer_context()
        context['req_user'] = req_user
        serializer = OrganizationCreateForUserSerializer(data=request_serializer.validated_data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        manual_parameters=[organization_id_header],
        request_body=ActivateSubscriptionSerializer,
        responses={
            status.HTTP_200_OK: OrganizationReadSerializer,
            status.HTTP_400_BAD_REQUEST: exceptions.BadRequestResponseSerializer,
        },
    )
    @action(methods=['post'], detail=True)
    def activate_subscription(self, request, pk=None):
        """Активировать подписку."""
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)  # noqa: DAR401
        serializer.is_valid(raise_exception=True)
        tariff = serializer.validated_data['tariff']
        if instance.balance < tariff.amount:
            raise ValidationError({'error': config.ORG_ACTIVATE_SUB_INSUFFICIENT_FUNDS_ERROR})
        active_subscription = instance.subscriptions.filter(is_active=True).first()
        if active_subscription:
            if active_subscription.tariff == tariff:
                raise ValidationError({'error': config.ORG_ACTIVATE_SUB_ALREADY_HAVE_SUB_ERROR})
            active_subscription.is_active = False
            active_subscription.auto_renewal = False
            active_subscription.save()
        ActivateSubscriptionService(tariff, instance, request.user).process()
        return Response(
            OrganizationReadSerializer(instance=instance, context=self.get_serializer_context()).data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        manual_parameters=[organization_id_header],
        request_body=EmptySerializer,
        responses={
            status.HTTP_200_OK: OrganizationReadSerializer,
            status.HTTP_400_BAD_REQUEST: exceptions.BadRequestResponseSerializer,
        },
    )
    @action(methods=['post'], detail=True)
    def deactivate_subscription(self, request, pk=None):
        """Деактивировать подписку."""
        instance = self.get_object()
        active_subscription = instance.subscriptions.filter(is_active=True).first()
        if active_subscription:
            active_subscription.is_active = False
            active_subscription.auto_renewal = False
            active_subscription.save()
        return Response(
            OrganizationReadSerializer(instance=instance, context=self.get_serializer_context()).data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        request_body=OrganizationOnlyINNWriteSerializer,
        responses={
            status.HTTP_200_OK: OrganizationInfoSerializer,
            status.HTTP_400_BAD_REQUEST: exceptions.BadRequestResponseSerializer,
        },
    )
    @action(['POST'], detail=False, url_path='find_organization_by_inn')
    def find_organization_by_inn(self, request):
        """Найти организацию по переданному ИНН, используется при создании организации."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # noqa: DAR401

        dadata_response = DadataFindByINNService().process(serializer.data.get('inn'))
        if not dadata_response:
            raise ValidationError({'error': config.ORG_NOT_FOUND_BY_INN_DADATA_ERROR})

        serializer = OrganizationInfoSerializer(dadata_response[0])
        return Response(serializer.data)

    @swagger_auto_schema(request_body=no_body, responses={
        status.HTTP_200_OK: CeleryResultSerializer,
        status.HTTP_400_BAD_REQUEST: exceptions.BadRequestResponseSerializer,
    })
    @action(methods=['post'], detail=False, url_path='export_excel')
    def admin_export_excel(self, request):
        """Выгрузить организации в excel файл."""
        host = f'{request.scheme}://{request.get_host()}'
        task = organizations_export_excel_task.delay(host)
        return Response({'result_id': task.id}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=no_body, responses={
        status.HTTP_200_OK: OrganizationReadSerializer,
        status.HTTP_400_BAD_REQUEST: exceptions.BadRequestResponseSerializer,
    })
    @action(methods=['post'], detail=True)
    def make_active(self, request, *args, **kwargs):
        """Сделать организацию активной у авторизованного юзера."""
        user = request.user
        instance = self.get_object()
        membership = instance.membership_set.filter(user=user).first()
        membership.is_active = True
        membership.save()
        serializer = OrganizationReadSerializer(instance=instance, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)
