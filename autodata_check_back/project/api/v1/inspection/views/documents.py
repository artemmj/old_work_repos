from rest_framework import permissions

from api.v1.inspection.serializers.documents import DocumentsReadSerializer, DocumentsWriteSerializer
from apps.helpers.viewsets import ExtendedModelViewSet
from apps.inspection.models.documents import Documents


class DocumentViewSet(ExtendedModelViewSet):
    """Документы."""

    queryset = Documents.objects.all()
    serializer_class = DocumentsWriteSerializer
    serializer_class_map = {
        'list': DocumentsReadSerializer,
        'create': DocumentsWriteSerializer,
        'retrieve': DocumentsReadSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
