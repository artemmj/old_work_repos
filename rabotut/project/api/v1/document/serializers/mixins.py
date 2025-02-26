from drf_yasg.utils import swagger_serializer_method

from api.v1.file.serializers import FileSerializer


class ListFileFieldMixin:
    """
    Для всех документов необходимо вернуть массив файлов.

    Только у регистрации может быть несколько, у остальных по 1 файлу.
    """

    @swagger_serializer_method(serializer_or_field=FileSerializer(many=True))
    def get_file(self, instance):
        return [FileSerializer(instance.file).data] if instance.file else []
