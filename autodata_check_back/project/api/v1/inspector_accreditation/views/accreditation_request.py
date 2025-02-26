from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.inspector.serializers import RequisiteSerializer
from api.v1.inspector_accreditation.filters.accreditation_request import AccreditationRequestFilterSet
from api.v1.inspector_accreditation.serializers import (
    InspectorAccreditationRequestCreateSerializer,
    InspectorAccreditationRequestReadSerializer,
)
from apps.helpers.exceptions import BadRequestResponseSerializer
from apps.helpers.permissions import IsAdministrator, IsCustomer, IsDispatcher, IsSuperUser
from apps.helpers.serializers import EnumSerializer
from apps.helpers.viewsets import CRUDExtendedModelViewSet
from apps.inspector_accreditation.models import InspectorAccreditationRequest, StatusChoices
from apps.inspector_accreditation.services import BindRequisiteService


class InspectorAccreditationRequestViewSet(CRUDExtendedModelViewSet):
    queryset = InspectorAccreditationRequest.objects.all()
    serializer_class = InspectorAccreditationRequestReadSerializer
    serializer_class_map = {
        'create': InspectorAccreditationRequestCreateSerializer,
        'update': InspectorAccreditationRequestCreateSerializer,
        'partial_update': InspectorAccreditationRequestCreateSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
    permission_map = {
        'create': (IsCustomer | IsSuperUser | IsAdministrator | IsDispatcher),
        'update': (IsCustomer | IsSuperUser | IsAdministrator | IsDispatcher),
        'partial_update': (IsCustomer | IsSuperUser | IsAdministrator | IsDispatcher),
        'destroy': (IsSuperUser | IsAdministrator | IsDispatcher),
    }
    search_fields = (
        'user__first_name',
        'user__last_name',
        'inn',
        'work_skills',
        'company',
        'city__title',
        'radius',
        'availability_thickness_gauge',
    )
    filterset_class = AccreditationRequestFilterSet
    ordering_fields = (
        'user__first_name',
        'user__last_name',
        'inn',
        'work_skills',
        'company',
        'city__title',
        'radius',
        'availability_thickness_gauge',
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        if IsCustomer().has_permission(self.request, self):
            queryset = queryset.filter(user=self.request.user)
        return queryset

    @swagger_auto_schema(
        request_body=InspectorAccreditationRequestCreateSerializer,
        responses={
            status.HTTP_201_CREATED: InspectorAccreditationRequestReadSerializer,
            status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            InspectorAccreditationRequestReadSerializer(instance=instance).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @swagger_auto_schema(
        request_body=InspectorAccreditationRequestCreateSerializer,
        responses={
            status.HTTP_200_OK: InspectorAccreditationRequestReadSerializer,
        },
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}  # noqa: WPS437
        return Response(
            InspectorAccreditationRequestCreateSerializer(instance=instance).data, status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: EnumSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
        },
    )
    @action(['GET'], detail=False, url_path='task_statuses')
    def task_statuses(self, request):
        return Response(EnumSerializer(StatusChoices, many=True).data)

    @swagger_auto_schema(
        request_body=RequisiteSerializer,
        responses={
            status.HTTP_200_OK: RequisiteSerializer,
            status.HTTP_400_BAD_REQUEST: BadRequestResponseSerializer,
        },
    )
    @action(['POST'], detail=False, url_path='bind_requisites')
    def bind_requisites(self, request):
        serializer = RequisiteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        BindRequisiteService(user=request.user, serializer_data=serializer.data).process()
        return Response(serializer.data, status=status.HTTP_200_OK)
