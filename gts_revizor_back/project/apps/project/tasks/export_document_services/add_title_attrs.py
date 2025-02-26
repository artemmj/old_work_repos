from typing import Dict

from api.v1.product.services.get_title_attrs import GetProductTitleAttrsService
from apps.helpers.services import AbstractService


class AddTitleAttrsService(AbstractService):
    def process(self, export_content: Dict, product_id: str, project_id: str) -> Dict:
        additional_title_attrs = GetProductTitleAttrsService(
            product_id=product_id,
            project_id=project_id,
            is_hidden=False,
        ).process()

        if additional_title_attrs:
            for idx, additional_title_attr in enumerate(additional_title_attrs, 1):
                export_content[f'pin_additional_title_{idx}'] = additional_title_attr.content

        hidden_title_attrs = GetProductTitleAttrsService(
            product_id=product_id,
            project_id=project_id,
            is_hidden=True,
        ).process()

        if hidden_title_attrs:
            for idx, hidden_title_attr in enumerate(hidden_title_attrs, 1):
                export_content[f'pin_hidden_title_attr_{idx}'] = hidden_title_attr.content

        return export_content
