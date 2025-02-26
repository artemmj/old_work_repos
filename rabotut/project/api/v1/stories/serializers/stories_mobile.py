from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from api.v1.file.serializers import ImageSerializer
from api.v1.news.serializers.news_mobile import NewsMobileCompactSerializer
from apps.stories.models import Stories


class StoriesMobileSerializer(serializers.ModelSerializer):
    preview = ImageSerializer()
    slides = ImageSerializer(many=True)
    news = NewsMobileCompactSerializer()
    read_stories = serializers.SerializerMethodField()

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
            'read_stories',
        )

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField())
    def get_read_stories(self, instance):
        return getattr(instance, 'read_stories', None)
