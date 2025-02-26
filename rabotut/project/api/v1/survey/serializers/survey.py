from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.file.serializers import ImageSerializer
from apps.survey.models import BaseSurveyMailing, Survey

from .question import QuestionCreateSerializer, QuestionSerializer


class SurveySerializer(serializers.ModelSerializer):
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


class SurveyRetrieveSerializer(serializers.ModelSerializer):
    preview_standart = ImageSerializer()
    preview_square = ImageSerializer()
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = (
            'id',
            'name',
            'preview_standart',
            'preview_square',
            'is_self_option',
            'questions',
        )


class SurveyCreateSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=True)

    class Meta:
        model = Survey
        fields = (
            'id',
            'name',
            'preview_standart',
            'preview_square',
            'is_self_option',
            'questions',
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        questions = validated_data.pop('questions')
        is_self_option = validated_data.get('is_self_option')
        if not is_self_option and not questions:
            raise ValidationError({
                'questions': 'Для создания опроса требуется передать вопросы либо разрешить свой вариант.',
            })
        new_survey = super().create(validated_data=validated_data)
        for question in questions:
            question['survey'] = new_survey.pk
            question_serializer = QuestionCreateSerializer(data=question)
            question_serializer.is_valid(raise_exception=True)
            question_serializer.save()
        return new_survey


class SurveyUpdateSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=True)

    class Meta:
        model = Survey
        fields = (
            'id',
            'name',
            'preview_standart',
            'preview_square',
            'is_self_option',
            'questions',
        )
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        mailing = BaseSurveyMailing.objects.filter(survey=instance).first()
        # Опрос создается сразу вместе с рассылкой с фронта с админки, поэтому mailing всегда должен быть
        if mailing and mailing.is_published:
            raise ValidationError('Невозможно обновить, опрос уже был опубликован.')

        questions = None
        # Если в PATCH запросе есть questions - обновить вопросы
        # пачкой, т.к. на фронте можно поменять вопросы в любой новой комбинации
        if 'questions' in validated_data:
            questions = validated_data.pop('questions')
        # Сначала обновить поля
        updated_survey = super().update(instance, validated_data)
        if questions:
            # Затем вопросы, если есть
            updated_survey.questions.all().delete(force=True)
            for question in questions:
                question['survey'] = updated_survey.pk
                new_question_serializer = QuestionCreateSerializer(data=question)
                new_question_serializer.is_valid(raise_exception=True)
                new_question_serializer.save()
        return updated_survey


class SurveyListIdSerializer(serializers.Serializer):
    surveys_ids = serializers.PrimaryKeyRelatedField(
        queryset=Survey.objects.values_list('id', flat=True),
        many=True,
        required=True,
    )
