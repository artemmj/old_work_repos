from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.survey.models import Answer, Option


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            'id',
            'user',
            'question',
            'options',
            'self_option_answer',
        )


class AnswerCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    option = serializers.PrimaryKeyRelatedField(queryset=Option.objects.all(), required=False)
    self_option_answer = serializers.CharField(required=False)

    class Meta:
        model = Answer
        fields = (
            'user',
            'question',
            'option',
            'self_option_answer',
        )

    def validate(self, attrs):
        question = attrs.get('question')
        survey = question.survey
        option = attrs.get('option')
        self_option_answer = attrs.get('self_option_answer')

        # Не передали ни варианта, ни своего ответа
        if not option and not self_option_answer:
            raise ValidationError({'option': 'Не выбран вариант ответа или не дан свой ответ.'})
        # В опросе запрещены свои ответы, не передали никакой вариант
        if not survey.is_self_option and not option:
            raise ValidationError({'option': 'Требуется передать доступный вариант.'})
        # Передали и вариант ответа, и свой ответ
        if option and self_option_answer:
            raise ValidationError({'option': 'Требуется передать какой-то один вариант ответа.'})
        return attrs
