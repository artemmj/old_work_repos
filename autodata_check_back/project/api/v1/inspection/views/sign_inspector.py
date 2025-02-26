from rest_framework import permissions

from api.v1.inspection.serializers.sign_inspector import SignInspectorCreateSerializer, SignInspectorRetrieveSerializer
from apps.helpers.viewsets import ExtendedModelViewSet
from apps.inspection.models.sign_inspector import SignInspector


class SignInspectorViewSet(ExtendedModelViewSet):
    queryset = SignInspector.objects.all()
    serializer_class = SignInspectorRetrieveSerializer
    serializer_class_map = {
        'create': SignInspectorCreateSerializer,
        'update': SignInspectorCreateSerializer,
        'partial_update': SignInspectorCreateSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
