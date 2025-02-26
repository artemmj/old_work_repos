import logging

from django.db.models import Prefetch

from apps.helpers.services import AbstractService
from apps.product.models import AdditionalProductTitleAttribute
from apps.project.models import Project

logger = logging.getLogger('django')


class GetProductsForListOfDiscrepanciesReportsService(AbstractService):  # noqa: WPS118
    """Сервис для получения продуктов проекта для генерации отчета "Концепт групп"."""

    def __init__(self, project: Project):
        self.project = project

    def process(self, *args, **kwargs):
        return (
            self.project.products
            .filter(remainder__isnull=False, remainder_2__isnull=False)
            .prefetch_related(
                Prefetch(
                    'title_attrs',
                    queryset=AdditionalProductTitleAttribute.objects.filter(is_hidden=False).only('content'),
                    to_attr='additional_title_attrs',
                ),
                Prefetch(
                    'title_attrs',
                    queryset=AdditionalProductTitleAttribute.objects.filter(is_hidden=True).only('content'),
                    to_attr='hide_title_attrs',
                ),
            )
        )
