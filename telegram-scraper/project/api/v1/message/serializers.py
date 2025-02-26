from rest_framework import serializers

from api.v1.channel.serializers import ChannelSerializer
from api.v1.file.serializers import FileSerializer
from apps.message.models import Message


class MessageSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer()
    files = FileSerializer(many=True)

    class Meta:
        model = Message
        fields = ('id', 'ext_id', 'ext_date', 'created_at', 'link', 'text', 'channel', 'files')
