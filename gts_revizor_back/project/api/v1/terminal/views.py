from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.v1.terminal.filters import TerminalFilterSet
from api.v1.terminal.serializers import (
    TerminalConnectSerializer,
    TerminalReadSerializer,
    TerminalUpdateSerializer,
    TerminalWriteSerializer,
)
from api.v1.terminal.services import CheckTerminalNumberService, ConnTerminalEmployeeService
from apps.helpers.viewsets import ListCreateUpdateExtendedModelViewSet
from apps.terminal.models import Terminal


class TerminalViewSet(ListCreateUpdateExtendedModelViewSet):
    queryset = Terminal.objects.all()
    serializer_class = TerminalWriteSerializer
    serializer_class_map = {
        'list': TerminalReadSerializer,
        'connect': TerminalConnectSerializer,
        'partial_update': TerminalUpdateSerializer,
    }
    permission_classes = (permissions.AllowAny,)
    ordering_fields = ('number', 'ip_address', 'db_loading')
    filterset_class = TerminalFilterSet
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    http_method_names = ('get', 'post', 'patch')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if 'number' in request.data:
            CheckTerminalNumberService(
                number=request.data.get('number'),
                device_model=request.data.get('device_model'),
                created=True,
            ).process()
        serializer.save()
        return Response(TerminalReadSerializer(instance=serializer.instance).data)

    @action(['POST'], detail=False, url_path='connect', url_name='connect')
    def connect(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service_res = ConnTerminalEmployeeService().process(serializer.data)
        return Response(TerminalReadSerializer(service_res).data)

    def partial_update(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(Terminal, pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if 'number' in request.data:
            CheckTerminalNumberService(
                number=request.data.get('number'),
                device_model=instance.device_model,
                created=False,
            ).process()
        serializer.save()
        return Response(TerminalReadSerializer(instance=serializer.instance).data)
