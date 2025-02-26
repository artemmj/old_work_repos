from rest_framework import serializers

from apps.channel.models import Channel


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'created_at', 'link', 'is_active')
