from constance import admin
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from api.v1.settings.serializers import SettingsSerializer


class SettingsViewSet(viewsets.ViewSet):

    @swagger_auto_schema(
        operation_summary='Список настроек.',
        responses={
            status.HTTP_200_OK: SettingsSerializer(many=True),
        },
    )
    def list(self, request):
        """Список настроек."""
        serializer = SettingsSerializer(admin.get_values().items(), many=True)
        return Response(serializer.data)
