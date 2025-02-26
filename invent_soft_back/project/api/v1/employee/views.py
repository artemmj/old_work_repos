from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from api.v1.employee.filters import EmployeeFilterSet
from api.v1.employee.serializers import (
    EmployeeBulkCreateSerializer,
    EmployeeBulkDeleteSerializer,
    EmployeeExportRequestSerializer,
    EmployeeReadSerializer,
    EmployeeRetrieveSerializer,
)
from apps.employee.managers import EmployeeManager
from apps.employee.models import Employee, EmployeeRoleChoices
from apps.employee.services.get_employees import GetEmployeesService
from apps.employee.tasks import export_employees
from apps.helpers.celery import CeleryResultSerializer
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.serializers import EnumSerializer
from apps.helpers.viewsets import ListRetrieveUpdateExtendedModelViewSet
from apps.task.models import Task, TaskStatusChoices


class EmployeeViewSet(ListRetrieveUpdateExtendedModelViewSet):
    serializer_class = EmployeeReadSerializer
    serializer_class_map = {
        'retrieve': EmployeeRetrieveSerializer,
        'bulk_create': EmployeeBulkCreateSerializer,
        'bulk_delete': EmployeeBulkDeleteSerializer,
        'export_employees': EmployeeExportRequestSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
    permission_map = {
        'list': permissions.AllowAny,
        'retrieve': permissions.AllowAny,
    }
    ordering_fields = ('serial_number', 'username', 'roles', 'is_auto_assignment')
    filterset_class = EmployeeFilterSet
    filter_backends = (DjangoFilterBackend, OrderingFilter)

    def get_queryset(self):
        return GetEmployeesService().process()

    @swagger_auto_schema(responses={
        200: EnumSerializer(many=True),
        404: ErrorResponseSerializer,
    })
    @action(methods=['get'], detail=False)
    def roles_choices(self, request):
        roles = [
            {'value': role[0], 'name': role[1]}
            for role in EmployeeRoleChoices.choices
            if role[0] == EmployeeRoleChoices.COUNTER
        ]
        return Response(roles)

    @swagger_auto_schema(
        request_body=EmployeeBulkCreateSerializer,
        responses={200: None, 400: ErrorResponseSerializer},
    )
    @action(methods=['post'], detail=False)
    def bulk_create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        EmployeeManager().bulk_create(serializer.validated_data)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=EmployeeBulkDeleteSerializer,
        responses={200: None, 400: ErrorResponseSerializer},
    )
    @action(methods=['post'], detail=False)
    def bulk_delete(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        EmployeeManager().bulk_delete(serializer.validated_data)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=EmployeeExportRequestSerializer, responses={200: CeleryResultSerializer})
    @action(methods=['post'], detail=False, url_path='export_to_file')
    def export_employees(self, request):
        """Выгрузка отчета по сотрудникам в файл."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.validated_data['project']
        host = f'{request.scheme}://{request.get_host()}'
        task = export_employees.delay(str(project.id), host)
        return Response({'result_id': task.id}, status=status.HTTP_200_OK)
