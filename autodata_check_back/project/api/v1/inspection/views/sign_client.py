from rest_framework import permissions

from api.v1.inspection.serializers.sign_client import SignClientCreateSerializer, SignClientRetrieveSerializer
from apps.helpers.viewsets import ExtendedModelViewSet
from apps.inspection.models.sign_client import SignClient


class SignClientViewSet(ExtendedModelViewSet):
    queryset = SignClient.objects.all()
    serializer_class = SignClientRetrieveSerializer
    serializer_class_map = {
        'create': SignClientCreateSerializer,
        'update': SignClientCreateSerializer,
        'partial_update': SignClientCreateSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
