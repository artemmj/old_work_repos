from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response

from api.v1.inspector_accreditation.serializers import (
    AccreditationInspectionReadSerializer,
    AccreditationInspectionWriteSerializer,
)
from apps.helpers.permissions import IsAdministrator, IsCustomer, IsDispatcher, IsSuperUser
from apps.helpers.viewsets import RUDExtendedModelViewSet
from apps.inspector_accreditation.models import AccreditationInspection


class AccreditationInspectionViewSet(RUDExtendedModelViewSet):
    queryset = AccreditationInspection.objects.all()
    serializer_class = AccreditationInspectionWriteSerializer
    serializer_class_map = {
        'list': AccreditationInspectionReadSerializer,
        'retrieve': AccreditationInspectionReadSerializer,
        'update': AccreditationInspectionWriteSerializer,
        'partial_update': AccreditationInspectionWriteSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
    permission_map = {
        'create': (IsCustomer | IsSuperUser | IsAdministrator | IsDispatcher),
        'update': (IsCustomer | IsSuperUser | IsAdministrator | IsDispatcher),
        'partial_update': (IsCustomer | IsSuperUser | IsAdministrator | IsDispatcher),
        'destroy': (IsSuperUser | IsAdministrator | IsDispatcher),
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if IsCustomer().has_permission(self.request, self):
            queryset = queryset.filter(accreditation_requests__user=self.request.user)
        return queryset

    @swagger_auto_schema(
        request_body=AccreditationInspectionWriteSerializer,
        responses={
            status.HTTP_200_OK: AccreditationInspectionReadSerializer,
        },
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}  # noqa: WPS437
        return Response(AccreditationInspectionReadSerializer(instance=instance).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=AccreditationInspectionWriteSerializer,
        responses={
            status.HTTP_200_OK: AccreditationInspectionReadSerializer,
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, args, kwargs)
