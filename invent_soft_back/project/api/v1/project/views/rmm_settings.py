from rest_framework import permissions

from api.v1.project.serializers.rmm_settings import RMMSettingsReadSerializer, RMMSettingsUpdateSerializer
from apps.helpers.viewsets import RUExtendedModelViewSet
from apps.project.models import RMMSettings


class RMMSettingsViewSet(RUExtendedModelViewSet):
    queryset = RMMSettings.objects.all()
    serializer_class = RMMSettingsUpdateSerializer
    serializer_class_map = {
        'retrieve': RMMSettingsReadSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
