from rest_framework import serializers

from api.v1.inspection_task.serializers.task import InspectionTaskReadSerializer
from apps.inspection_task.models.invitation import Invitation


class InvitationReadSerializer(serializers.ModelSerializer):
    task = InspectionTaskReadSerializer()

    class Meta:
        model = Invitation
        fields = ('id', 'task', 'is_accepted')
