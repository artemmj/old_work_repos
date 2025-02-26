from apps.helpers.services import AbstractService
from apps.template.models import TemplateField


class CopyTemplateFieldsToDbService(AbstractService):
    """Сервис для копирования полей шаблона в базу данных."""

    def __init__(self, template_fields):
        self.template_fields = template_fields

    def process(self):
        TemplateField.objects.all().delete()
        for field_value, field_name in self.template_fields:
            is_reusable = 'pin_' in field_value

            TemplateField.objects.update_or_create(
                name=field_name,
                value=field_value,
                is_reusable=is_reusable,
            )
