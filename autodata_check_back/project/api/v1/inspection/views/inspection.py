from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from api.v1.inspection.filters.inspection import InspectionFilterSet
from api.v1.inspection.serializers.inspection import (
    InspectionAdminCompactQuerySerializer,
    InspectionAdminCompactSerializer,
    InspectionCompactSerializer,
    InspectionReadSerializer,
    InspectionsListSerializer,
    InspectionWriteSerializer,
    LeaveNoteSerializer,
)
from apps.helpers.exceptions import BadRequestResponseSerializer
from apps.helpers.permissions import (
    IsAdministrator,
    IsDispatcher,
    IsOrganizationManager,
    IsOrganizationOwner,
    IsSuperUser,
)
from apps.helpers.serializers import EnumSerializer
from apps.helpers.viewsets import ExtendedModelViewSet, paginate_response
from apps.inspection.models.inspection import Inspection, InspectionTypes, StatusChoices
from apps.organization.models.organization import Organization


class InspectionViewSet(ExtendedModelViewSet):  # noqa: WPS214
    queryset = Inspection.objects.all()
    serializer_class = InspectionWriteSerializer
    serializer_class_map = {
        'list': InspectionReadSerializer,
        'list_short': InspectionCompactSerializer,
        'create': InspectionWriteSerializer,
        'retrieve': InspectionReadSerializer,
        'admin_compact': InspectionAdminCompactSerializer,
        'leave_note': LeaveNoteSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
    permission_map = {
        'admin_compact': (IsSuperUser | IsAdministrator | IsDispatcher),
        'retrieve': permissions.AllowAny,
    }
    filterset_class = InspectionFilterSet
    search_fields = (
        'car__brand__title',
        'car__model__title',
        'car__vin_code',
        'inspector__first_name',
        'inspector__last_name',
        'organization__title',
        'complete_date',
        'status',
        'organization__self_inspection_price',
        'is_public',
        'created_at',
        'car__gov_number',
    )
    ordering_fields = (
        'car__brand__title',
        'car__model__title',
        'car__vin_code',
        'inspector__first_name',
        'inspector__last_name',
        'organization__title',
        'complete_date',
        'status',
        'organization__self_inspection_price',
        'is_public',
        'created_at',
        'car__gov_number',
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    @swagger_auto_schema(responses={
        status.HTTP_201_CREATED: InspectionReadSerializer,
        status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
    })
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(InspectionReadSerializer(instance).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if (  # noqa: WPS337
            instance.is_public  # noqa: WPS408, WPS222
            or (
                not instance.is_public and  # noqa: WPS222, W504
                (instance.task and instance.task.author == request.user)
                or instance.inspector == request.user
                or (IsOrganizationOwner | IsOrganizationManager)().has_permission(request, self)
                or (IsAdministrator | IsDispatcher)().has_permission(request, self)
            )
        ):
            return super().retrieve(request, args, kwargs)
        raise PermissionDenied({'error': 'У вас нет прав для выполнения этой операции.'})

    @swagger_auto_schema(responses={status.HTTP_200_OK: InspectionCompactSerializer})
    @action(detail=False, methods=['GET'], url_path='list_short')
    def list_short(self, request):
        """Урезанный список осмотров."""
        queryset = self.filter_queryset(self.get_queryset())
        return paginate_response(self, queryset=queryset, context=self.get_serializer_context())

    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumSerializer})
    @action(methods=['get'], detail=False)
    def statuses(self, request):
        """Возвращает возможные типы статусов осмотра."""
        return Response(EnumSerializer(StatusChoices, many=True).data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumSerializer(many=True)})
    @action(methods=['get'], detail=False)
    def types(self, request):
        """Возвращает возможные типы осмотров."""
        return Response(EnumSerializer(InspectionTypes, many=True).data)

    @swagger_auto_schema(
        query_serializer=InspectionAdminCompactQuerySerializer,
        responses={
            status.HTTP_200_OK: InspectionAdminCompactSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
        },
    )
    @action(methods=['get'], detail=False, url_path='admin/compact')
    def admin_compact(self, request):
        """Список осмотров с урезанными данными для админки."""
        query_serializer = InspectionAdminCompactQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        query_user = query_serializer.validated_data.get('user', None)
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(task__isnull=True)
        if query_user:
            queryset = queryset.filter(inspector=query_user)
        return paginate_response(self, queryset)

    @swagger_auto_schema(
        request_body=LeaveNoteSerializer,
        responses={
            status.HTTP_201_CREATED: LeaveNoteSerializer(),
            status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
        },
    )
    @action(methods=['post'], detail=False, url_path='leave_note')
    def leave_note(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(LeaveNoteSerializer(instance).data, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False, url_path='inspections_list')
    def inspections_list(self, request, *args, **kwargs):
        """Для экрана Отчеты админки."""
        queryset = self.filter_queryset(self.get_queryset())

        if self.request.organization:
            queryset = queryset.filter(task__organization=request.organization)
        # NOTE: нужно фронтам, так шлют
        if 'organization' in self.request.query_params:
            organization = Organization.objects.filter(pk=self.request.query_params.get('organization')).first()
            if organization:
                queryset = queryset.filter(task__organization=organization)

        return paginate_response(self, queryset, InspectionsListSerializer, context=self.get_serializer_context())
