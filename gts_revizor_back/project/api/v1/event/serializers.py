from rest_framework import serializers

from apps.event.models import Event, TitleChoices
from apps.helpers.serializers import EnumField


class EventSerializer(serializers.ModelSerializer):
    title = EnumField(enum_class=TitleChoices)

    class Meta:
        model = Event
        fields = ('id', 'fake_id', 'created_at', 'title', 'comment')
