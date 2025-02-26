from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from api.v1.file.serializers import FileSerializer, ImageSerializer
from api.v1.news.serializers.news_emoji import NewsEmojiSerializer
from apps.news.models import News, NewsEmoji
from apps.news.models.ext import EmojiChoices


class NewsAllEmojiSerializer(serializers.Serializer):
    emoji_type = serializers.ChoiceField(choices=EmojiChoices, source='value')
    count = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField())
    def get_count(self, instance):
        return NewsEmoji.objects.filter(news=self.context['news'], emoji_type=instance).count()


class NewsMobileSerializer(serializers.ModelSerializer):
    preview_standard = ImageSerializer()
    preview_main = ImageSerializer(required=False)
    user_emoji = serializers.SerializerMethodField()
    all_emoji = serializers.SerializerMethodField()
    read_news = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = (
            'id',
            'name',
            'text',
            'preview_standard',
            'preview_main',
            'user_emoji',
            'all_emoji',
            'created_at',
            'read_news',
        )

    @swagger_serializer_method(serializer_or_field=NewsEmojiSerializer)
    def get_user_emoji(self, instance):
        user = self.context['request'].user
        user_emoji = NewsEmoji.objects.filter(news=instance, user=user).first()
        return NewsEmojiSerializer(instance=user_emoji).data

    @swagger_serializer_method(serializer_or_field=NewsAllEmojiSerializer(many=True))
    def get_all_emoji(self, instance):
        return NewsAllEmojiSerializer(EmojiChoices, many=True, context={'news': instance}).data

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField())
    def get_read_news(self, instance):
        return getattr(instance, 'read_news', None)


class NewsMobileRetrieveSerializer(NewsMobileSerializer):
    attachments = FileSerializer(many=True)
    read_news = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = (
            'id',
            'name',
            'text',
            'preview_standard',
            'preview_main',
            'user_emoji',
            'all_emoji',
            'created_at',
            'read_news',
            'attachments',
        )

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField())
    def get_read_news(self, instance):
        return getattr(instance, 'read_news', None)


class NewsMobileCompactSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'name')
