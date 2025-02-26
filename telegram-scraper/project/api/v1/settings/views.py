from constance import admin
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.response import Response

from api.v1.settings.serializers import SettingsSerializer


class SettingsViewSet(viewsets.ViewSet):

    @swagger_auto_schema(responses={200: SettingsSerializer(many=True)})
    def list(self, request):
        serializer = SettingsSerializer(admin.get_values().items(), many=True)
        return Response(serializer.data)
