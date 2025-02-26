from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from api.v1.file.serializers import FileSerializer, ImageSerializer
from apps.promotion.models import Promotion


class PromotionSerializer(serializers.ModelSerializer):
    preview_standart = ImageSerializer()
    preview_main = ImageSerializer()
    attachments = FileSerializer(many=True)
    attachments_count = serializers.SerializerMethodField()

    class Meta:
        model = Promotion
        fields = (
            'id',
            'created_at',
            'updated_at',
            'name',
            'text',
            'preview_standart',
            'preview_main',
            'attachments',
            'attachments_count',
            'is_top',
        )

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField())
    def get_attachments_count(self, obj):   # noqa: WPS110
        return obj.attachments.count()


class PromotionRetrieveSerializer(PromotionSerializer):
    class Meta:
        model = Promotion
        fields = (
            'id',
            'created_at',
            'updated_at',
            'end_date',
            'name',
            'text',
            'preview_standart',
            'preview_main',
            'attachments',
            'type',
            'is_top',
            'is_main_display',
            'is_hidden',
        )


class PromotionListIdSerializer(serializers.Serializer):
    promotion_ids = serializers.PrimaryKeyRelatedField(
        queryset=Promotion.objects.values_list('id', flat=True),
        many=True,
        required=True,
    )


class PromotionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = (
            'id',
            'end_date',
            'name',
            'text',
            'preview_standart',
            'preview_main',
            'attachments',
            'type',
            'is_top',
            'is_main_display',
            'is_hidden',
        )
        read_only_fields = ('id',)


class PromotionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = (
            'id',
            'end_date',
            'name',
            'text',
            'preview_standart',
            'preview_main',
            'attachments',
            'type',
            'is_top',
            'is_main_display',
            'is_hidden',
        )
        read_only_fields = ('id',)
