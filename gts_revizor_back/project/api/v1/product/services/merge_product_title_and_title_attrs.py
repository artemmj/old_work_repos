from django.db.models import QuerySet

from api.v1.product.services import ConvertAdditionalTitleAttrsToStrService, ConvertHiddenTitleAttrsToStrService
from apps.helpers.services import AbstractService


class MergeProductTitleAndTitleAttrsService(AbstractService):
    """Сервис для объединения названия продукта и его доп. аттрибутов."""

    def __init__(
        self,
        additional_title_attrs: QuerySet,
        hidden_title_attrs: QuerySet,
        product_title: str,
    ):
        self.additional_title_attrs = additional_title_attrs
        self.hidden_title_attrs = hidden_title_attrs
        self.product_title = product_title

    def process(self, *args, **kwargs):
        converted_additional_title_attrs = ConvertAdditionalTitleAttrsToStrService(
            additional_title_attrs=self.additional_title_attrs,
        ).process()

        converted_hidden_title_attrs = ConvertHiddenTitleAttrsToStrService(
            hidden_title_attrs=self.hidden_title_attrs,
        ).process()

        if self.additional_title_attrs and self.hidden_title_attrs:
            return '{0}{1} {2}'.format(
                self.product_title,
                converted_additional_title_attrs,
                converted_hidden_title_attrs,
            )

        if self.additional_title_attrs:
            return '{0}{1}'.format(self.product_title, converted_additional_title_attrs)

        if self.hidden_title_attrs:
            return '{0} {1}'.format(self.product_title, converted_hidden_title_attrs)

        return self.product_title
