from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from api.v1.file.serializers import FileSerializer, ImageSerializer
from apps.news.models import News, NewsRead


class NewsSerializer(serializers.ModelSerializer):
    preview_standard = ImageSerializer()
    preview_main = ImageSerializer()
    attachments = FileSerializer(many=True)
    attachments_count = serializers.SerializerMethodField()
    news_read_count = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = (
            'id',
            'name',
            'text',
            'preview_standard',
            'preview_main',
            'created_at',
            'attachments',
            'attachments_count',
            'news_read_count',
            'is_top',
            'is_main_page',
        )

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField())
    def get_attachments_count(self, obj):   # noqa: WPS110
        return obj.attachments.count()

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField())
    def get_news_read_count(self, obj):   # noqa: WPS110
        return NewsRead.objects.filter(news=obj).count()


class NewsRetrieveSerializer(NewsSerializer):
    class Meta:
        model = News
        fields = (
            'id',
            'name',
            'text',
            'preview_standard',
            'preview_main',
            'created_at',
            'updated_at',
            'attachments',
            'is_top',
            'is_main_page',
        )


class NewsListIdSerializer(serializers.Serializer):
    news_ids = serializers.PrimaryKeyRelatedField(
        queryset=News.objects.values_list('id', flat=True),
        many=True,
        required=True,
    )


class NewsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'name', 'text', 'preview_standard', 'preview_main', 'attachments', 'is_top', 'is_main_page')
        read_only_fields = ('id',)


class NewsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'name', 'text', 'preview_standard', 'preview_main', 'attachments', 'is_top', 'is_main_page')
        read_only_fields = ('id',)
