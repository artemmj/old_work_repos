from rest_framework import serializers


class FileArketaSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    file = serializers.FileField()  # noqa: WPS110
    extension = serializers.CharField()
    name = serializers.CharField()
    created_at = serializers.DateTimeField()


class FileArketaExtendedSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    file = serializers.FileField(required=False)  # noqa: WPS110
    extension = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(required=False)
    size = serializers.FloatField(required=False)
    human_size = serializers.FloatField(required=False)


class TaskFileSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    file = serializers.CharField()  # noqa: WPS110


class FileArketaUploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)  # noqa: WPS110
