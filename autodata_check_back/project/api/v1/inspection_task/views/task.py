from constance import config
from django.db.models import Count, Q  # noqa: WPS347
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.v1.inspection_task.filters.task import InspectionTaskFilterSet
from api.v1.inspection_task.serializers import (
    InspectionTaskAdminCompactQuerySerializer,
    InspectionTaskAdminCompactSerializer,
    InspectionTaskAppointmentSerializer,
    InspectionTaskCarSerializer,
    InspectionTaskReadSerializer,
    InspectionTaskWriteSerializer,
)
from apps.helpers.celery import CeleryResultSerializer
from apps.helpers.exceptions import BadRequestResponseSerializer
from apps.helpers.permissions import IsAdministrator, IsCustomer, IsDispatcher, IsSuperUser
from apps.helpers.serializers import EnumSerializer
from apps.helpers.viewsets import ExtendedModelViewSet, paginate_response
from apps.inspection_task.models.task import InspectionTask, InspectorTaskStatuses, InspectorTaskTypes
from apps.inspection_task.tasks import inspection_tasks_export_excel


class InspectionTaskViewSet(ExtendedModelViewSet):  # noqa: WPS214
    queryset = InspectionTask.objects.all()
    serializer_class = InspectionTaskReadSerializer
    serializer_class_map = {
        'create': InspectionTaskWriteSerializer,
        'update': InspectionTaskWriteSerializer,
        'partial_update': InspectionTaskWriteSerializer,
        'admin_compact': InspectionTaskAdminCompactSerializer,
        'appointment_organization_inspector': InspectionTaskAppointmentSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
    permission_map = {
        'create': (IsCustomer | IsSuperUser | IsAdministrator | IsDispatcher),
        'update': (IsCustomer | IsSuperUser | IsAdministrator | IsDispatcher),
        'partial_update': (IsCustomer | IsSuperUser | IsAdministrator | IsDispatcher),
        'destroy': (IsCustomer | IsSuperUser | IsAdministrator | IsDispatcher),
        'create_cars': IsCustomer,
        'admin_compact': (IsSuperUser | IsAdministrator | IsDispatcher),
        'inspector_search_stop': (IsAdministrator | IsDispatcher),
    }
    filterset_class = InspectionTaskFilterSet
    search_fields = (
        'author__first_name',
        'author__last_name',
        'author__phone',
        'inspection_task_cars__vin_code',
        'inspection_task_cars__brand__title',
        'inspection_task_cars__model__title',
        'inspector__first_name',
        'inspector__last_name',
        'organization__title',
        'end_date',
        'created_at',
        'status',
        'organization__self_inspection_price',
    )
    ordering_fields = (
        'author__first_name',
        'author__last_name',
        'author__phone',
        'inspection_task_cars__vin_code',
        'inspection_task_cars__brand__title',
        'inspection_task_cars__model__title',
        'inspector__first_name',
        'inspector__last_name',
        'cars_count',
        'organization__title',
        'end_date',
        'created_at',
        'planed_date',
        'status',
        'organization__self_inspection_price',
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        if (IsSuperUser | IsAdministrator | IsDispatcher)().has_permission(self.request, self):
            return queryset
        return queryset.filter(Q(author=self.request.user) | Q(inspector=self.request.user))  # noqa: WPS221

    @swagger_auto_schema(responses={
        status.HTTP_201_CREATED: InspectionTaskReadSerializer,
        status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
    })
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(InspectionTaskReadSerializer(instance).data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: InspectionTaskReadSerializer,
        status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
    })
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}  # noqa: WPS437
        return Response(InspectionTaskReadSerializer(instance).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumSerializer(many=True)})
    @action(methods=['get'], detail=False)
    def types(self, request):
        """Возвращает возможные типы осмотров."""
        return Response(EnumSerializer(InspectorTaskTypes, many=True).data)

    @swagger_auto_schema(
        request_body=no_body,
        responses={
            status.HTTP_200_OK: InspectionTaskReadSerializer,
            status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
        },
    )
    @action(methods=['post'], detail=True)
    def inspector_search(self, request, pk=None):
        """Поиск инспектора."""
        instance = self.get_object()
        instance.status = InspectorTaskStatuses.INSPECTOR_SEARCH
        instance.save()
        return Response(InspectionTaskReadSerializer(instance=instance).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=no_body,
        responses={
            status.HTTP_200_OK: InspectionTaskReadSerializer,
            status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
        },
    )
    @action(methods=['post'], detail=True)
    def inspector_search_stop(self, request, pk=None):
        """Отмена поиска инспектора."""
        instance = self.get_object()
        if instance.status != InspectorTaskStatuses.INSPECTOR_SEARCH:  # noqa: DAR401
            raise ValidationError({'error': config.TASK_NOT_INSPECTOR_SEARCH_BY_TASK_ERROR})
        instance.status = InspectorTaskStatuses.DRAFT
        instance.save()
        return Response(InspectionTaskReadSerializer(instance=instance).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=InspectionTaskAppointmentSerializer,
        responses={
            status.HTTP_200_OK: InspectionTaskReadSerializer,
            status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
        },
    )
    @action(['POST'], detail=True)
    def appointment_organization_inspector(self, request, pk=None):
        """Назначить инспектора организации."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        inspector = serializer.validated_data.get('inspector')

        instance = self.get_object()
        instance.status = InspectorTaskStatuses.TASK_ACCEPTED
        instance.type = InspectorTaskTypes.FOR_APPOINTMENT
        instance.inspector = inspector
        instance.save()
        return Response(InspectionTaskReadSerializer(instance=instance).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=InspectionTaskCarSerializer(many=True),
        responses={
            status.HTTP_201_CREATED: InspectionTaskReadSerializer,
            status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
        },
    )
    @action(methods=['post'], detail=True)
    def create_cars(self, request, pk=None):
        """Создание автомобилей и их добавление к заданию."""
        instance = self.get_object()
        context = self.get_serializer_context()
        context['task'] = instance
        serializer = InspectionTaskCarSerializer(data=request.data, context=context, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance.refresh_from_db()
        return Response(InspectionTaskReadSerializer(instance).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={
            status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
        },
    )
    @action(methods=['delete'], detail=True)
    def delete_cars(self, request, pk=None):
        """Удалить автомобили задания."""
        instance = self.get_object()
        if instance.status != InspectorTaskStatuses.DRAFT:  # noqa: DAR401
            raise ValidationError({'error': config.TASK_DELETE_CARS_BUT_NON_DRAFT_ERROR})
        instance.inspection_task_cars.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumSerializer})
    @action(methods=['get'], detail=False, filterset_class=None)
    def statuses(self, request):
        """Возвращает возможные статусы заданий."""
        return Response(EnumSerializer(InspectorTaskStatuses, many=True).data)

    @swagger_auto_schema(
        query_serializer=InspectionTaskAdminCompactQuerySerializer,
        responses={
            status.HTTP_200_OK: InspectionTaskAdminCompactSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
        },
    )
    @action(methods=['get'], detail=False, url_path='admin/compact')
    def admin_compact(self, request):
        """Список заданий с урезанными данными для админки."""
        query_serializer = InspectionTaskAdminCompactQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        query_user = query_serializer.validated_data.get('user', None)
        queryset = self.filter_queryset(self.get_queryset())
        if query_user:
            queryset = queryset.filter(author=query_user)
        queryset = queryset.annotate(cars_count=Count('inspection_task_cars'))
        return paginate_response(self, queryset)

    @swagger_auto_schema(request_body=no_body, responses={
        status.HTTP_200_OK: CeleryResultSerializer,
        status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
    })
    @action(methods=['post'], detail=False, url_path='export_excel')
    def inspection_tasks_export_excel(self, request):
        """Генерация отчета на задания по осмотрам организации."""
        host = f'{request.scheme}://{request.get_host()}'
        task = inspection_tasks_export_excel.delay(
            host,
            request.organization.pk if request.organization else None,
        )
        return Response({'result_id': task.id}, status=status.HTTP_200_OK)
