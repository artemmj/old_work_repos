from rest_framework import serializers

from apps.helpers.serializers import EnumField
from apps.promotion.models import EmojiChoices, PromotionEmoji


class PromotionEmojiSerializer(serializers.ModelSerializer):
    emoji_type = EnumField(enum_class=EmojiChoices)

    class Meta:
        model = PromotionEmoji
        fields = ('id', 'emoji_type')


class PromotionEmojiPostSerializer(serializers.Serializer):
    emoji_type = serializers.ChoiceField(choices=EmojiChoices, required=True)
