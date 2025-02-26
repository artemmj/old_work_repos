from rest_framework import serializers

from ..answer import RecognitionAnswerSerializer, ScannerAnswerSerializer
from ..file import TaskFileSerializer


class TaskArketaAnswerWriteSerializer(serializers.Serializer):
    numeric = serializers.FloatField(required=False)
    monetary = serializers.FloatField(required=False)
    boolean = serializers.BooleanField(required=False)
    textual = serializers.CharField(required=False)
    photo = TaskFileSerializer(many=True, required=False)
    date = serializers.DateField(required=False)
    choice = serializers.CharField(required=False)
    multi_choice = serializers.ListField(child=serializers.CharField(), required=False)
    recognition = RecognitionAnswerSerializer(required=False)
    scanner = ScannerAnswerSerializer(many=True, required=False)
    id = serializers.UUIDField()
    visit = serializers.IntegerField(required=False)
    client_created_at = serializers.DateTimeField()


class TaskArketaAnswerWriteRequestSerializer(serializers.Serializer):
    answers = TaskArketaAnswerWriteSerializer(many=True)
