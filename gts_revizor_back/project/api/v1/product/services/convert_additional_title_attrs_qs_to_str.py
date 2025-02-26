from typing import List

from apps.helpers.services import AbstractService
from apps.product.models import AdditionalProductTitleAttribute


class ConvertAdditionalTitleAttrsToStrService(AbstractService):
    """Сервис для преобразования списка доп. аттрибутов названия продукта в строку."""

    def __init__(self, additional_title_attrs: List[AdditionalProductTitleAttribute], delimiter: str = ','):
        self.additional_title_attrs = additional_title_attrs
        self.delimiter = delimiter

    def process(self, *args, **kwargs):
        additional_title_attrs_content = [
            additional_title_attr.content
            for additional_title_attr in self.additional_title_attrs
        ]

        return f'{self.delimiter} ' + f'{self.delimiter} '.join(list(additional_title_attrs_content))
