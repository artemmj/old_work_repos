from rest_framework import serializers

from apps.helpers.serializers import PointExtField


class VisitArketaSerializer(serializers.Serializer):
    client_start = serializers.DateTimeField()
    client_end = serializers.DateTimeField()
    task = serializers.UUIDField()
    start_location = PointExtField(required=False)
    end_location = PointExtField(required=False)
    receipt_photo = serializers.UUIDField(required=False)
    schedule_photo = serializers.UUIDField()


class VisitArketaResponseSerializer(VisitArketaSerializer):
    id = serializers.UUIDField(required=False)
