from typing import Dict, List

from apps.helpers.services import AbstractService
from apps.survey.models import Answer


class SendSurveyReplyService(AbstractService):
    """
    Сервис записывает ответы на вопросы опроса.

    Данные приходят уже валидированные из сериалайзера.
    """

    def process(self, answers: List[Dict]) -> List[Answer]:
        new_answers = []
        for answer in answers:
            answer_data = {'user': answer.get('user'), 'question': answer.get('question')}
            if 'self_option_answer' in answer:
                answer_data['self_option_answer'] = answer.get('self_option_answer')
            new_answer = Answer.objects.create(**answer_data)
            if 'option' in answer:
                new_answer.options.add(answer.get('option'))
                new_answer.save()
            new_answers.append(new_answer)
        return new_answers
