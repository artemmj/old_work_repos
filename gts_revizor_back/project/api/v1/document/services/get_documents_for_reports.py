import logging
from typing import Dict

from django.db.models import Prefetch

from apps.document.models import Document
from apps.helpers.services import AbstractService
from apps.product.models import AdditionalProductTitleAttribute

logger = logging.getLogger('django')


class GetDocumentsForReportsService(AbstractService):
    """Сервис для получения документов для генерации отчетов."""

    def __init__(self, documents_filter_params: Dict):
        self.documents_filter_params = documents_filter_params

    def process(self, *args, **kwargs):
        return (
            Document
            .objects
            .filter(**self.documents_filter_params)
            .prefetch_related(
                'counter_scan_task__scanned_products__product',
                Prefetch(
                    'counter_scan_task__scanned_products__product__title_attrs',
                    queryset=AdditionalProductTitleAttribute.objects.filter(is_hidden=False).only('content'),
                    to_attr='additional_title_attrs',
                ),
                Prefetch(
                    'counter_scan_task__scanned_products__product__title_attrs',
                    queryset=AdditionalProductTitleAttribute.objects.filter(is_hidden=True).only('content'),
                    to_attr='hide_title_attrs',
                ),
            )
        )
