from api.v1.message.filters import MessageFilterSet
from api.v1.message.serializers import MessageSerializer
from apps.helpers.viewsets import LRExtendedModelViewSet
from apps.message.models import Message


class MessageViewSet(LRExtendedModelViewSet):
    queryset = Message.objects.all().order_by('-ext_date')
    serializer_class = MessageSerializer
    filterset_class = MessageFilterSet
    search_fields = ('text', 'channel__link')
    ordering_fields = ('created_at', 'ext_date')
