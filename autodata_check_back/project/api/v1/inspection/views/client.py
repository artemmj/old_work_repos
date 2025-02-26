from rest_framework import permissions

from api.v1.inspection.serializers.client import ClientReadSerializer, ClientWriteSerializer
from apps.helpers.viewsets import ExtendedModelViewSet
from apps.inspection.models.client import Client


class ClientViewSet(ExtendedModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientWriteSerializer
    serializer_class_map = {
        'list': ClientReadSerializer,
        'retrieve': ClientReadSerializer,
        'create': ClientWriteSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
