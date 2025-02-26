from django.db.models import QuerySet

from apps.helpers.services import AbstractService


class ConvertHiddenTitleAttrsQsToStrService(AbstractService):
    """Сервис для преобразования списка скрытых аттрибутов названия продукта в строку."""

    def __init__(self, hidden_title_attrs_qs: QuerySet, delimiter: str = ','):
        self.hidden_title_attrs_qs = hidden_title_attrs_qs
        self.delimiter = delimiter

    def process(self, *args, **kwargs):
        hidden_title_attrs = self.hidden_title_attrs_qs.values_list('content', flat=True)

        return '(' + f'{self.delimiter} '.join(list(hidden_title_attrs)) + ')'
