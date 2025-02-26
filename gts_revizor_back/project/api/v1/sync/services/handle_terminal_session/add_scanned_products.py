from decimal import Decimal
from typing import List

from apps.helpers.services import AbstractService
from apps.product.models import Product, ScannedProduct
from apps.task.models import Task


class AddScanProdsToTaskService(AbstractService):
    """Сервис для добавления отсканированных товаров в таску (для счетчика, аудитора и внешнего аудитора)."""

    def __init__(self, db_task: Task, scan_prods: List):
        self.db_task = db_task
        self.scan_prods = scan_prods

    def process(self):
        for scanned in self.scan_prods:
            # Пытаемся найти товар по полному совпадению, либо ставим как неизвестный
            barcode = scanned['product']
            if scanned.get('is_weight_product', False):
                barcode = scanned['product'][:7]

            attempt_products = Product.objects.filter(
                project=self.db_task.zone.project,
                title=scanned.get('title', None),
                barcode=barcode,
                vendor_code=scanned.get('vendor_code', None),
                qr_code=scanned.get('qr_code', ''),
            )

            if attempt_products:
                db_product = attempt_products.first()
            else:
                db_product, _ = Product.objects.get_or_create(
                    barcode=scanned['product'],
                    vendor_code=f'art_{scanned["product"]}',
                    title='Неизвестный товар',
                    project=self.db_task.zone.project,
                )

            amount = scanned.get('amount')
            if scanned.get('is_weight_product', False):  # весовой товар, в килограммы
                amount = Decimal(amount / 1000)

            scan_prd_create_data = {
                'product': db_product,
                'task': self.db_task,
                'defaults': {
                    'amount': amount,
                    'added_by_product_code': scanned.get('added_by_product_code'),
                    'added_by_qr_code': scanned.get('added_by_qr_code'),
                    'is_weight': scanned.get('is_weight_product'),
                    'scanned_time': scanned.get('scanned_time'),
                },
            }
            if scanned.get('dm', None):
                scan_prd_create_data['dm'] = scanned.get('dm')
            newscanned, created = ScannedProduct.objects.get_or_create(**scan_prd_create_data)
            if not created:
                newscanned.amount += amount
                newscanned.save(update_fields=['amount'])
            self.db_task.result += amount

        self.db_task.result = round(self.db_task.result, 3)
        self.db_task.save(update_fields=['result'])
