from django.db.models import QuerySet

from apps.helpers.services import AbstractService


class ConvertAdditionalTitleAttrsQsToStrService(AbstractService):
    """Сервис для преобразования списка доп. аттрибутов названия продукта в строку."""

    def __init__(self, additional_title_attrs_qs: QuerySet, delimiter: str = ','):
        self.additional_title_attrs_qs = additional_title_attrs_qs
        self.delimiter = delimiter

    def process(self, *args, **kwargs):
        additional_title_attrs = self.additional_title_attrs_qs.values_list('content', flat=True)

        return f'{self.delimiter} ' + f'{self.delimiter} '.join(list(additional_title_attrs))
