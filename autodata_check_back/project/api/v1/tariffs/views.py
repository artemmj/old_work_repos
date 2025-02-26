from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions

from api.v1.tariffs.serializers import TariffReadSerializer, TariffWriteSerializer
from apps.helpers.permissions import (
    IsAdministrator,
    IsDispatcher,
    IsOrganizationManager,
    IsOrganizationOwner,
    IsSuperUser,
)
from apps.helpers.swagger import organization_id_header
from apps.helpers.viewsets import ExtendedModelViewSet
from apps.tariffs.models import Tariff


class TariffViewSet(ExtendedModelViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffReadSerializer
    serializer_class_map = {
        'create': TariffWriteSerializer,
        'update': TariffWriteSerializer,
        'partial_update': TariffWriteSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
    permission_map = {
        'create': (IsSuperUser | IsDispatcher | IsAdministrator),
        'update': (IsSuperUser | IsDispatcher | IsAdministrator),
        'partial_update': (IsSuperUser | IsDispatcher | IsAdministrator),
        'destroy': (IsSuperUser | IsDispatcher | IsAdministrator),
        'activate_subscription': (IsOrganizationOwner | IsOrganizationManager),
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if (IsSuperUser | IsDispatcher | IsAdministrator)().has_permission(self.request, self):
            return queryset
        if queryset.filter(organization=self.request.organization).exists():
            return queryset.filter(organization=self.request.organization)
        return queryset.filter(organization__isnull=True)

    @swagger_auto_schema(manual_parameters=[organization_id_header])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)
