from apps.helpers.services import AbstractService
from apps.template.models import TemplateField


class GetUniqueTemplateFieldsService(AbstractService):
    """Сервис для получения уникальных полей шаблона."""

    def process(self):
        return (
            TemplateField
            .objects
            .exclude(value__contains='pin_not_download_')
            .exclude(value__contains='pin_additional_title_')
            .exclude(value__contains='pin_hidden_title_attr_')
        )
