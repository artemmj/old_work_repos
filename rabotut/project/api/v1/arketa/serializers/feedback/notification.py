from rest_framework import serializers


class FeedbackArketaNotificationQuerySerializer(serializers.Serializer):
    unread_exists = serializers.BooleanField(required=False)
    search = serializers.CharField(required=False)
    limit = serializers.IntegerField(required=False)
    offset = serializers.IntegerField(required=False)
