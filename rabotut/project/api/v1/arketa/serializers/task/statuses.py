from rest_framework import serializers


class TaskArketaStatusesSerializer(serializers.Serializer):
    value = serializers.CharField()  # noqa: WPS110
    name = serializers.CharField()
    count = serializers.IntegerField()
