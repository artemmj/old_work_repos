from rest_framework import serializers

from apps.survey.models import Question

from .option import OptionCreateSerializer, OptionSerializer


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'number', 'name', 'options')
        read_only_fields = ('id',)


class QuestionCreateSerializer(serializers.ModelSerializer):
    options = OptionCreateSerializer(many=True, required=True, allow_empty=False)

    class Meta:
        model = Question
        fields = ('number', 'name', 'survey', 'options')

    def create(self, validated_data):
        options = validated_data.pop('options')
        new_question = super().create(validated_data=validated_data)
        for option in options:
            option['question'] = new_question.pk
            option_serializer = OptionCreateSerializer(data=option)
            option_serializer.is_valid(raise_exception=True)
            option_serializer.save()
        return new_question
