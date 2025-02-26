from rest_framework import serializers

from apps.survey.models import Option, Question


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'number', 'name')
        read_only_fields = ('id',)


class OptionCreateSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=False)

    class Meta:
        model = Option
        fields = ('number', 'name', 'question')
