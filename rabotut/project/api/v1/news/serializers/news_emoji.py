from rest_framework import serializers

from apps.helpers.serializers import EnumField
from apps.news.models import EmojiChoices, NewsEmoji


class NewsEmojiSerializer(serializers.ModelSerializer):
    emoji_type = EnumField(enum_class=EmojiChoices)

    class Meta:
        model = NewsEmoji
        fields = ('id', 'emoji_type')


class NewsEmojiPostSerializer(serializers.Serializer):
    emoji_type = serializers.ChoiceField(choices=EmojiChoices, required=True)
