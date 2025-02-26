from typing import List

from apps.helpers.services import AbstractService
from apps.product.models import AdditionalProductTitleAttribute


class ConvertHiddenTitleAttrsToStrService(AbstractService):
    """Сервис для преобразования списка скрытых аттрибутов названия продукта в строку."""

    def __init__(self, hidden_title_attrs: List[AdditionalProductTitleAttribute], delimiter: str = ','):
        self.hidden_title_attrs = hidden_title_attrs
        self.delimiter = delimiter

    def process(self, *args, **kwargs):
        hidden_title_attrs_content = [
            hidden_title_attr.content
            for hidden_title_attr in self.hidden_title_attrs
        ]
        return '(' + f'{self.delimiter} '.join(list(hidden_title_attrs_content)) + ')'
