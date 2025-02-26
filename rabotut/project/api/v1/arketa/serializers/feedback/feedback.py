from rest_framework import serializers

from api.v1.arketa.serializers.task.task import TaskArketaMobileCompactSerializer


class FeedbackArketaMobileNotificationSerializer(serializers.Serializer):
    task = TaskArketaMobileCompactSerializer()
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)
    name = serializers.CharField(required=False)
    unread_exists = serializers.BooleanField()


class FeedbackArketaCreateSerializer(serializers.Serializer):
    task = serializers.UUIDField()
    estimation = serializers.IntegerField()
    comment = serializers.CharField()
    files = serializers.ListField(child=serializers.UUIDField(), required=False)
