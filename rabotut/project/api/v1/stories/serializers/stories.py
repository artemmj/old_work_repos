from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from api.v1.file.serializers import ImageSerializer
from api.v1.news.serializers.news_mobile import NewsMobileCompactSerializer
from apps.stories.models import Stories, StoriesRead


class StoriesSerializer(serializers.ModelSerializer):
    preview = ImageSerializer()
    stories_read_count = serializers.SerializerMethodField()

    class Meta:
        model = Stories
        fields = ('id', 'name', 'preview', 'news', 'stories_read_count', 'is_top')

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField())
    def get_stories_read_count(self, obj):  # noqa: WPS110
        return StoriesRead.objects.filter(stories=obj).count()


class StoriesRetrieveSerializer(StoriesSerializer):
    slides = ImageSerializer(many=True)
    news = NewsMobileCompactSerializer()

    class Meta:
        model = Stories
        fields = (
            'id',
            'name',
            'preview',
            'slides',
            'news',
            'background_color_button',
            'text_color',
            'text_button',
            'is_top',
        )


class StoriesListIdSerializer(serializers.Serializer):
    stories_ids = serializers.PrimaryKeyRelatedField(
        queryset=Stories.objects.values_list('id', flat=True),
        many=True,
        required=True,
    )


class StoriesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stories
        fields = (
            'id',
            'name',
            'preview',
            'slides',
            'news',
            'background_color_button',
            'text_color',
            'text_button',
            'is_top',
        )
        read_only_fields = ('id',)


class StoriesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stories
        fields = (
            'id',
            'name',
            'preview',
            'slides',
            'news',
            'background_color_button',
            'text_color',
            'text_button',
            'is_top',
        )
        read_only_fields = ('id',)


class StoriesViewsReportRequestSerializer(serializers.Serializer):
    start = serializers.DateField(required=True)
    end = serializers.DateField(required=True)
