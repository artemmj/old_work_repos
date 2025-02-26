from jinja2.filters import do_filesizeformat
from rest_framework import serializers

from apps.file.models import DBFile, File, Image, StaticFile
from apps.file.validator import ImageExtensionValidator


class FileSerializer(serializers.ModelSerializer):
    file_name = serializers.SerializerMethodField(read_only=True)
    file_size = serializers.SerializerMethodField(read_only=True, help_text='Размер файла, kB')
    human_size = serializers.SerializerMethodField(read_only=True, help_text='Читаемый размер файла')
    file = serializers.FileField(required=True)  # noqa: WPS110

    class Meta:
        model = File
        fields = (
            'id',
            'file',
            'file_name',
            'file_size',
            'human_size',
        )

        read_only_fields = ('id', 'file_name', 'file_size', 'human_size')

    def get_file_name(self, obj):  # noqa: WPS110
        return obj.file.name

    def get_file_size(self, obj) -> float:  # noqa: WPS110
        try:
            return obj.file.size / 1000
        except FileNotFoundError:
            return 0

    def get_human_size(self, obj) -> str:  # noqa: WPS110
        try:
            return do_filesizeformat(obj.file.size)
        except FileNotFoundError:
            return '0 kB'


class ImageSerializer(serializers.ModelSerializer):
    image_name = serializers.SerializerMethodField(read_only=True)
    image_size = serializers.SerializerMethodField(read_only=True, help_text='Размер файла, kB')
    human_size = serializers.SerializerMethodField(read_only=True, help_text='Читаемый размер файла')
    image = serializers.FileField(
        required=True,
        validators=[ImageExtensionValidator(allowed_extensions=('jpg', 'jpeg', 'webp', 'png', 'gif', 'svg'))],
    )

    class Meta:
        model = Image
        fields = (
            'id',
            'image',
            'image_name',
            'image_size',
            'human_size',
        )

        read_only_fields = ('id', 'file_name', 'file_size', 'human_size')

    def get_image_name(self, obj):  # noqa: WPS110
        return obj.image.name

    def get_image_size(self, obj) -> float:  # noqa: WPS110
        try:
            return obj.image.size / 1000
        except FileNotFoundError:
            return 0

    def get_human_size(self, obj) -> str:  # noqa: WPS110
        try:
            return do_filesizeformat(obj.image.size)
        except FileNotFoundError:
            return '0 kB'


class DBFileSerializer(serializers.ModelSerializer):
    file_name = serializers.SerializerMethodField(read_only=True)
    file_size = serializers.SerializerMethodField(read_only=True, help_text='Размер файла, kB')
    human_size = serializers.SerializerMethodField(read_only=True, help_text='Читаемый размер файла')

    class Meta:
        model = DBFile
        fields = ('id', 'created_at', 'file', 'file_name', 'file_size', 'human_size')

    def get_file_name(self, obj):  # noqa: WPS110
        return obj.file.name

    def get_file_size(self, obj) -> float:  # noqa: WPS110
        try:
            return obj.file.size / 1000
        except FileNotFoundError:
            return 0

    def get_human_size(self, obj) -> str:  # noqa: WPS110
        try:
            return do_filesizeformat(obj.file.size)
        except FileNotFoundError:
            return '0 kB'


class StaticFileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True)  # noqa: WPS110

    class Meta:
        model = StaticFile
        fields = (
            'id',
            'file',
            'type',
        )
        read_only_fields = ('id',)
