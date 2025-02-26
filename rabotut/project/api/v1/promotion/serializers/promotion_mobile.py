from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from api.v1.file.serializers import FileSerializer, ImageSerializer
from apps.promotion.models import Promotion, PromotionEmoji
from apps.promotion.models.ext import EmojiChoices

from .promotion_emoji import PromotionEmojiSerializer


class PromotionAllEmojiSerializer(serializers.Serializer):
    emoji_type = serializers.ChoiceField(choices=EmojiChoices, source='value')
    count = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField())
    def get_count(self, instance):
        return PromotionEmoji.objects.filter(promotion=self.context['promotion'], emoji_type=instance).count()


class PromotionMobileSerializer(serializers.ModelSerializer):
    preview_standart = ImageSerializer()
    preview_main = ImageSerializer(required=False)
    user_emoji = serializers.SerializerMethodField()
    all_emoji = serializers.SerializerMethodField()
    read_promotions = serializers.SerializerMethodField()

    class Meta:
        model = Promotion
        fields = (
            'id',
            'name',
            'text',
            'preview_standart',
            'preview_main',
            'user_emoji',
            'all_emoji',
            'created_at',
            'end_date',
            'read_promotions',
        )

    @swagger_serializer_method(serializer_or_field=PromotionEmojiSerializer)
    def get_user_emoji(self, instance):   # noqa: WPS110
        user = self.context['request'].user
        user_emoji = PromotionEmoji.objects.filter(promotion=instance, user=user).first()
        return PromotionEmojiSerializer(instance=user_emoji).data

    @swagger_serializer_method(serializer_or_field=PromotionAllEmojiSerializer(many=True))
    def get_all_emoji(self, instance):   # noqa: WPS110
        return PromotionAllEmojiSerializer(EmojiChoices, many=True, context={'promotion': instance}).data

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField())
    def get_read_promotions(self, instance):
        return getattr(instance, 'read_promotions', None)


class PromotionMobileRetrieveSerializer(PromotionMobileSerializer):
    attachments = FileSerializer(many=True)
    read_promotions = serializers.SerializerMethodField()

    class Meta:
        model = Promotion
        fields = (
            'id',
            'name',
            'text',
            'preview_standart',
            'preview_main',
            'user_emoji',
            'all_emoji',
            'created_at',
            'end_date',
            'read_promotions',
            'attachments',
        )

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField())
    def get_read_promotions(self, instance):
        return getattr(instance, 'read_promotions', None)
