from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from api.v1.reports.services.inventory_in_zones_in_zones_report import inventory_in_zones_in_zones_report_celery_wrapper
from api.v1.zone.filters.filters import ZoneFilterSet
from api.v1.zone.serializers import (  # noqa: WPS235
    BatchIssuingTasksSerializer,
    InventoryInZonesReportRequestSerializer,
    RolesZoneReadSerializer,
    StorageNamesSerializer,
    ZoneAutoAssignmentTasksSerializer,
    ZoneBlockStatisticResponseSerializer,
    ZoneBulkCreateSerializer,
    ZoneBulkDeleteSerializer,
    ZoneBulkUpdateRangeSerializer,
    ZoneBulkUpdateSelectSerializer,
    ZoneIssuingTasksSerializer,
    ZoneReadSerializer,
    ZoneWriteSerializer,
)
from apps.employee.models import Employee
from apps.helpers.celery import CeleryResultSerializer
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.viewsets import ListUpdateExtendedModelViewSet, paginate_response
from apps.project.models import Project
from apps.task.models import TaskStatusChoices, TaskTypeChoices
from apps.zone.managers import ZoneManager
from apps.zone.models import Zone
from apps.zone.services import IssuingTasksService
from apps.zone.services.auto_assignment import AutoAssignmentZoneService
from apps.zone.services.batch_issuing_tasks import BatchIssuingTasksService
from apps.zone.services.bulk_update_storage_name_zone import BulkUpdateStorageNameZoneService
from apps.zone.services.get_zones import GetZonesService

from .ordering import ZoneOrderingAsIntService
from .services import ZoneStatisticBlockService


class ZoneViewSet(ListUpdateExtendedModelViewSet):  # noqa: WPS214
    serializer_class = ZoneWriteSerializer
    serializer_class_map = {
        'list': ZoneReadSerializer,
        'bulk_create': ZoneBulkCreateSerializer,
        'bulk_delete': ZoneBulkDeleteSerializer,
        'issuing_tasks': ZoneIssuingTasksSerializer,
        'auto_assignment_tasks': ZoneAutoAssignmentTasksSerializer,
        'storage_names': StorageNamesSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
    ordering_fields = ('serial_number', 'title', 'code', 'barcode_amount')
    filterset_class = ZoneFilterSet
    filter_backends = (DjangoFilterBackend, OrderingFilter)

    def get_queryset(self):
        return GetZonesService().process()

    def list(self, request):
        qs = ZoneOrderingAsIntService().process(
            qs=self.filter_queryset(self.get_queryset()),
            qp=request.query_params,
        )
        return paginate_response(self, qs, ZoneReadSerializer, context={'request': request})

    @swagger_auto_schema(
        request_body=None,
        responses={
            200: ZoneBlockStatisticResponseSerializer,
            400: ErrorResponseSerializer,
        },
    )
    @action(methods=['get'], detail=False)
    def block_statistic(self, request):
        qs = ZoneOrderingAsIntService().process(
            qs=self.filter_queryset(self.get_queryset()),
            qp=request.query_params,
        )
        serialiser = ZoneReadSerializer(qs, many=True, context={'request': request})
        result = ZoneStatisticBlockService(serializer_data=serialiser.data).process()
        return Response(result)

    @swagger_auto_schema(request_body=ZoneBulkCreateSerializer, responses={200: None, 400: ErrorResponseSerializer})
    @action(methods=['post'], detail=False)
    def bulk_create(self, request):
        """Создание зон."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ZoneManager().bulk_create(serializer.validated_data)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ZoneBulkDeleteSerializer, responses={200: None, 400: ErrorResponseSerializer})
    @action(methods=['post'], detail=False)
    def bulk_delete(self, request):
        """Удаление зон."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ZoneManager().bulk_delete(serializer.validated_data)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ZoneBulkUpdateRangeSerializer,
        responses={
            200: None,
            400: ErrorResponseSerializer,
        },
    )
    @action(methods=['patch'], detail=False)
    def bulk_update_storage_name_in_range(self, request):
        """Изменение названия складов в зонах в диапазоне"""
        serializer = ZoneBulkUpdateRangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project_id = serializer.data.get('project_id')
        storage_name = serializer.data.get('storage_name')
        start_serial_number = serializer.data.get('start_serial_number')
        end_serial_number = serializer.data.get('end_serial_number')

        filter_options = {
            'project_id': project_id,
            'serial_number__gte': start_serial_number,
            'serial_number__lte': end_serial_number,
        }

        BulkUpdateStorageNameZoneService().process(filter_options, storage_name)

        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ZoneBulkUpdateSelectSerializer,
        responses={
            200: None,
            400: ErrorResponseSerializer,
        },
    )
    @action(methods=['patch'], detail=False)
    def bulk_update_storage_name_select(self, request):
        """Изменение названия складов в зонах выборочно"""
        serializer = ZoneBulkUpdateSelectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project_id = serializer.data.get('project_id')
        storage_name = serializer.data.get('storage_name')
        zones_ids = serializer.data.get('zones_ids')

        filter_options = {
            'project_id': project_id,
            'pk__in': zones_ids,
        }

        BulkUpdateStorageNameZoneService().process(filter_options, storage_name)

        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ZoneIssuingTasksSerializer,
        responses={
            200: None,
            400: ErrorResponseSerializer,
        },
    )
    @action(methods=['post'], detail=True)
    def issuing_tasks(self, request, pk=None):
        """Выдача заданий."""
        zone = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employees = serializer.validated_data['employees']
        role = serializer.validated_data['role']
        IssuingTasksService(zone, employees, role).process()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=BatchIssuingTasksSerializer)
    @action(['POST'], False)  # noqa: WPS425
    def batch_issuing_tasks(self, request):
        """Выдача заданий разом на пачку зон."""
        serializer = BatchIssuingTasksSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project_id = serializer.data.get('project')
        project = Project.objects.get(id=project_id)

        if 'zone_start_id' in serializer.data and 'zone_end_id' in serializer.data:
            zones = Zone.objects.filter(
                project=project_id,
                serial_number__in=range(serializer.data.get('zone_start_id'), serializer.data.get('zone_end_id') + 1),
            )
        elif 'zones' in serializer.data:
            zones = Zone.objects.filter(pk__in=serializer.data.get('zones'))
        else:
            return Response(status=status.HTTP_200_OK)

        employees = Employee.objects.filter(pk__in=serializer.data.get('employee_ids'))

        BatchIssuingTasksService(
            zones=zones,
            employees=employees,
            role=serializer.data['role'],
            project=project,
        ).process()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ZoneAutoAssignmentTasksSerializer,
        responses={
            200: None,
            400: ErrorResponseSerializer,
        },
    )
    @action(methods=['post'], detail=False)
    def auto_assignment_tasks(self, request):
        """Авто выдача заданий."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.validated_data['project']
        AutoAssignmentZoneService(project).process()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: ZoneReadSerializer, 400: ErrorResponseSerializer},
    )
    @action(methods=['get'], detail=False, url_path='statistics')
    def roles_statistics(self, request):
        """Для экрана Роли."""
        qs = self.filter_queryset(
            self.get_queryset().filter(
                tasks__type=TaskTypeChoices.COUNTER_SCAN,
                tasks__status__in=(
                    TaskStatusChoices.WORKED,
                    TaskStatusChoices.SUCCESS_SCAN,
                    TaskStatusChoices.FAILED_SCAN,
                ),
            )).distinct()
        return paginate_response(self, qs, RolesZoneReadSerializer)

    @action(methods=['get'], detail=False)
    def storage_names(self, request):
        """Роут получения списка названий складов"""
        names = set(self.filter_queryset(self.get_queryset()).values_list('storage_name', flat=True))
        return Response({'storage_names': names}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=InventoryInZonesReportRequestSerializer(),
        responses={200: CeleryResultSerializer, 400: ErrorResponseSerializer},
    )
    @action(methods=['post'], detail=False, url_path='inventory_in_zones_in_zones')
    def inventory_in_zones(self, request):
        """Роут для формирования отчета Отчет данных инвентаризации по зонам."""
        serializer = InventoryInZonesReportRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pref = f'{request.scheme}://{request.META["HTTP_HOST"]}'
        task = inventory_in_zones_in_zones_report_celery_wrapper.delay(
            serializer_data=serializer.data,
            endpoint_pref=pref,
        )
        return Response({'task_id': task.id})
