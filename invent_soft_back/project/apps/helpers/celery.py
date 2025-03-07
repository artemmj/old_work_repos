from rest_framework import serializers


class CeleryResultSerializer(serializers.Serializer):
    result_id = serializers.UUIDField()


class CeleryTaskWrapper:
    def __init__(self, body_serializer, task, filename=None):  # noqa: D107
        self.body_serializer = body_serializer
        self.task = task
        self.filename = filename

    def execute(self, request) -> str:
        serializer = self.body_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        result = self.task.delay(**serializer.data)  # noqa: WPS110
        return result.id
