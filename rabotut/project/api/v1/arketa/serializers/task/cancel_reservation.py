from rest_framework import serializers


class TaskArketaCancelReservationSerializer(serializers.Serializer):
    decline_reason = serializers.CharField()
