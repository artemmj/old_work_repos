from rest_framework import serializers

from apps.file.models import File, Image
from apps.file.validator import ImageExtensionValidator


class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True)  # noqa: WPS110

    class Meta:
        model = File
        fields = (
            'id',
            'file',
        )

        read_only_fields = ('id',)


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.FileField(
        required=True,
        validators=[ImageExtensionValidator(allowed_extensions=('jpg', 'jpeg', 'webp', 'png', 'gif'))],
    )

    class Meta:
        model = Image
        fields = (
            'id',
            'image',
        )

        read_only_fields = ('id',)
