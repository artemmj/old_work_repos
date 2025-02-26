import os

from constance import admin
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.settings.serializers import BuildVersionSerializer, SettingsSerializer

BUILD_VER = os.getenv('BUILD_VER')


class SettingsViewSet(viewsets.ViewSet):

    @swagger_auto_schema(responses={200: SettingsSerializer(many=True)})
    def list(self, request):
        serializer = SettingsSerializer(admin.get_values().items(), many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: BuildVersionSerializer})
    @action(methods=['get'], detail=False)
    def build_version(self, request):
        return Response({'build_version': BUILD_VER})
