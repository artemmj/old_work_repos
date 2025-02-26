from django.db.models import QuerySet

from apps.helpers.services import AbstractService
from apps.product.models import AdditionalProductTitleAttribute


class GetProductTitleAttrsService(AbstractService):
    """Сервис получения доп. параметров названия продукта."""

    def __init__(self, project_id, product_id: str, is_hidden: bool):
        self.product_id = product_id
        self.project_id = project_id
        self.is_hidden = is_hidden

    def process(self, *args, **kwargs) -> QuerySet:
        return AdditionalProductTitleAttribute.objects.filter(
            project_id=self.project_id,
            product_id=self.product_id,
            is_hidden=self.is_hidden,
        )
