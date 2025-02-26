from rest_framework import serializers

from ..file import FileArketaSerializer


class FeedbackArketaMobileReadSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    task = serializers.UUIDField()
    comment = serializers.CharField()
    files = FileArketaSerializer(many=True)
    estimation = serializers.IntegerField()
    created_at = serializers.DateTimeField(required=False)
    type = serializers.CharField()
    status = serializers.CharField()
    was_seen_by_executor = serializers.BooleanField()


class TaskArketaFeedbackSerializer(serializers.Serializer):
    original_price = serializers.IntegerField()
    new_price = serializers.IntegerField()
    feedback_available = serializers.BooleanField()
    executor_can_comment = serializers.BooleanField()
    unread_exists = serializers.BooleanField()
    master_feedback = FeedbackArketaMobileReadSerializer()
    client_feedback = FeedbackArketaMobileReadSerializer()
    executor_feedback = FeedbackArketaMobileReadSerializer()


class TaskArketaFeedbackCompactSerializer(serializers.Serializer):
    original_price = serializers.IntegerField()
    new_price = serializers.IntegerField(allow_null=True)
