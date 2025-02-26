from api.v1.product.services import (
    ConvertAdditionalTitleAttrsQsToStrService,
    ConvertHiddenTitleAttrsQsToStrService,
    GetProductTitleAttrsService,
)
from apps.helpers.services import AbstractService


class MergeProductTitleAndTitleAttrsService(AbstractService):
    """Сервис для объединения названия продукта и его доп. аттрибутов."""

    def __init__(
        self,
        project_id: str,
        product_id: str,
        product_title: str,
    ):
        self.project_id = project_id
        self.product_id = product_id
        self.product_title = product_title

    def process(self, *args, **kwargs):
        additional_title_attrs = GetProductTitleAttrsService(
            project_id=self.project_id,
            product_id=self.product_id,
            is_hidden=False,
        ).process()
        converted_additional_title_attrs = ConvertAdditionalTitleAttrsQsToStrService(
            additional_title_attrs_qs=additional_title_attrs,
        ).process()

        hidden_title_attrs = GetProductTitleAttrsService(
            project_id=self.project_id,
            product_id=self.product_id,
            is_hidden=True,
        ).process()
        converted_hidden_title_attrs = ConvertHiddenTitleAttrsQsToStrService(
            hidden_title_attrs_qs=hidden_title_attrs,
        ).process()

        if additional_title_attrs and hidden_title_attrs:
            return '{0}{1} {2}'.format(
                self.product_title,
                converted_additional_title_attrs,
                converted_hidden_title_attrs,
            )

        if additional_title_attrs:
            return '{0}{1}'.format(self.product_title, converted_additional_title_attrs)

        if hidden_title_attrs:
            return '{0} {1}'.format(self.product_title, converted_hidden_title_attrs)

        return self.product_title
