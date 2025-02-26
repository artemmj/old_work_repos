from dataclasses import dataclass
from decimal import Decimal
from typing import List

from django.db.models import QuerySet

from apps.helpers.services import AbstractService


@dataclass
class ScannedProductsAttrs:
    titles: List[str]
    barcodes: List[str]
    amounts: List[Decimal]
    vendor_codes: List[str]
    prices: List[Decimal]
    dm_codes: List[str]
    store_numbers: List[int]
    remainders: List[Decimal]
    discrepancies: List[int]
    decimal_discrepancies: List[Decimal]
    zones_names: List[str]
    zones_numbers: List[int]
    zones_codes: List[str]
    documents_counter_codes: List[int]
    is_weight: List[bool]


class GetScannedProductsAttrsService(AbstractService):  # noqa: WPS214
    """Сервис получения атрибутов отсканированных товаров"""

    def __init__(self, scanned_products: QuerySet):
        self.scanned_products = scanned_products

    def process(self) -> ScannedProductsAttrs:
        return ScannedProductsAttrs(
            titles=self._get_titles(),
            barcodes=self._get_barcodes(),
            amounts=self._get_amounts(),
            vendor_codes=self._get_vendor_codes(),
            prices=self._get_prices(),
            dm_codes=self._get_dm_codes(),
            store_numbers=self._get_store_numbers(),
            remainders=self._get_remainders(),
            discrepancies=self._get_discrepancies(),
            decimal_discrepancies=self._get_decimal_discrepancies(),
            zones_names=self._get_zones_names(),
            zones_numbers=self._get_zones_numbers(),
            zones_codes=self._get_zones_codes(),
            documents_counter_codes=self._get_tsd_numbers(),
            is_weight=self._get_is_weight_attrs(),
        )

    def _get_is_weight_attrs(self):
        return list(self.scanned_products.values_list('is_weight', flat=True))

    def _get_tsd_numbers(self):
        return list(self.scanned_products.values_list('task__counter_scan_document__tsd_number', flat=True))

    def _get_zones_codes(self):
        return list(self.scanned_products.values_list('task__counter_scan_document__zone__code', flat=True))

    def _get_zones_numbers(self):
        return list(
            self.scanned_products.values_list(
                'task__counter_scan_document__zone__serial_number',
                flat=True,
            ),
        )

    def _get_zones_names(self):
        return list(self.scanned_products.values_list('task__counter_scan_document__zone__title', flat=True))

    def _get_decimal_discrepancies(self):
        return list(self.scanned_products.values_list('discrepancy_decimal', flat=True))

    def _get_discrepancies(self):
        return list(self.scanned_products.values_list('discrepancy', flat=True))

    def _get_remainders(self):
        return list(self.scanned_products.values_list('product__remainder', flat=True))

    def _get_store_numbers(self):
        return list(self.scanned_products.values_list('product__store_number', flat=True))

    def _get_dm_codes(self):
        return list(self.scanned_products.values_list('dm', flat=True))

    def _get_prices(self):
        return list(self.scanned_products.values_list('product__price', flat=True))

    def _get_vendor_codes(self):
        return list(self.scanned_products.values_list('product__vendor_code', flat=True))

    def _get_amounts(self):
        return list(self.scanned_products.values_list('amount', flat=True))

    def _get_titles(self):
        return list(self.scanned_products.values_list('product__title', flat=True))

    def _get_barcodes(self):
        return list(self.scanned_products.values_list('product__barcode', flat=True))
