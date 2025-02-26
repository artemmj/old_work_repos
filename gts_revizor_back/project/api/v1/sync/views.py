import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.v1.sync.serializers import (
    GetProjectDataRequestSerializer,
    GetProjectDataResponseSerializer,
    SendOfflineDataSerializer,
)
from api.v1.sync.services import generate_project_data
from api.v1.sync.services.handle_terminal_session.core import HandleTerminalSessionService
from api.v1.task.serializers import TaskReadSerializer

logger = logging.getLogger('django')


class SyncViewSet(ViewSet):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        query_serializer=GetProjectDataRequestSerializer,
        responses={200: GetProjectDataResponseSerializer},
    )
    @action(['GET'], False, 'get-project-data', 'get-project-data')  # noqa: WPS425
    def get_project_data(self, request):
        query_serializer = GetProjectDataRequestSerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        service_result = generate_project_data(query_serializer.data['project'])
        return Response(service_result)

    @swagger_auto_schema(
        request_body=SendOfflineDataSerializer,
        responses={200: TaskReadSerializer(many=True)},
    )
    @action(['POST'], False, 'send-offline-data', 'send-offline-data')  # noqa: WPS425
    def send_offline_data(self, request):
        serializer = SendOfflineDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service_result = HandleTerminalSessionService(serializer.data).process()
        return Response(service_result)
