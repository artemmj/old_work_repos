from typing import Dict, List

from apps.helpers.services import AbstractService
from apps.product.models import ScannedProduct


class BulkCreateScannedProductsService(AbstractService):
    """Сервис массового создания отсканированных продуктов."""

    def __init__(self, scanned_products_content: List[Dict]):
        self.scanned_products_content = scanned_products_content

    def process(self):
        ScannedProduct.objects.bulk_create(
            [
                ScannedProduct(
                    **scanned_product_content,
                )
                for scanned_product_content in self.scanned_products_content
            ],
            ignore_conflicts=True,
        )
