from api.v1.channel.serializers import ChannelSerializer
from apps.channel.models import Channel
from apps.helpers.viewsets import CRDExtendedModelViewSet


class ChannelViewSet(CRDExtendedModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
