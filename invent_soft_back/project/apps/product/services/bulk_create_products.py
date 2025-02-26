from typing import Dict, List

from apps.helpers.services import AbstractService
from apps.product.models import Product
from apps.project.models import Project


class BulkCreateProductsService(AbstractService):
    """Сервис массового создания продуктов."""

    def __init__(self, new_project: Project, products_content: List[Dict]):
        self.products_content = products_content
        self.new_project = new_project

    def process(self):
        Product.objects.bulk_create(
            [
                Product(
                    project=self.new_project,
                    **product_content,
                )
                for product_content in self.products_content
            ],
            ignore_conflicts=True,
        )
