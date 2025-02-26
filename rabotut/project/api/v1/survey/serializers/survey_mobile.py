from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.file.serializers import ImageSerializer
from apps.survey.models import Answer, Survey

from .answer import AnswerCreateSerializer
from .question import QuestionSerializer


class SurveyMobileSerializer(serializers.ModelSerializer):
    preview_standart = ImageSerializer()
    preview_square = ImageSerializer()

    class Meta:
        model = Survey
        fields = (
            'id',
            'created_at',
            'updated_at',
            'name',
            'preview_standart',
            'preview_square',
            'is_self_option',
        )


class SurveyMobileRetrieveSerializer(serializers.ModelSerializer):
    preview_standart = ImageSerializer()
    preview_square = ImageSerializer()
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = (
            'id',
            'created_at',
            'updated_at',
            'name',
            'preview_standart',
            'preview_square',
            'is_self_option',
            'questions',
        )


class SendSurveyReplySerializer(serializers.ModelSerializer):
    answers = AnswerCreateSerializer(many=True, required=True, allow_empty=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Survey
        fields = ('answers', 'user')

    def validate(self, attrs):
        survey = self.context.get('survey')
        answers = attrs.get('answers')

        # Проверить, что юзер не проходил этот опрос
        exist_user_answer = Answer.objects.filter(user=attrs.get('user'), question=answers[0].get('question')).exists()
        if exist_user_answer:
            raise ValidationError({'survey': 'Опрос уже был пройден.'})
        # Проверить чтобы кол-во ответов совпадало с кол-во вопросов в опросе
        if len(answers) != survey.questions.count():
            raise ValidationError({'answers': 'Необходимо передать все ответы на все вопросы опроса.'})
        # Проверить, что каждый вопрос принадлежит этому опросу
        for answer in answers:
            question = answer.get('question')
            if question.survey != survey:
                raise ValidationError({'question': f'Вопрос \"{question}\" не относится к опросу \"{survey}\"'})
        return attrs
