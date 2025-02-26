import logging

from django.db.models import Prefetch

from apps.helpers.services import AbstractService
from apps.product.models import AdditionalProductTitleAttribute
from apps.project.models import Project
from apps.task.models import Task

logger = logging.getLogger('django')


class GetZonesService(AbstractService):
    """Сервис для получения зон проекта."""

    def __init__(self, project: Project, zones_filter_params, tasks_filter_params):
        self.project = project
        self.zones_filter_params = zones_filter_params
        self.tasks_filter_params = tasks_filter_params

    def process(self, *args, **kwargs):
        return (
            self.project
            .zones
            .filter(**self.zones_filter_params)
            .prefetch_related(
                Prefetch(
                    'tasks',
                    queryset=Task.objects.filter(**self.tasks_filter_params),
                ),
                Prefetch(
                    'tasks__scanned_products__product__title_attrs',
                    queryset=AdditionalProductTitleAttribute.objects.filter(is_hidden=False).only('content'),
                    to_attr='additional_title_attrs',
                ),
                Prefetch(
                    'tasks__scanned_products__product__title_attrs',
                    queryset=AdditionalProductTitleAttribute.objects.filter(is_hidden=True).only('content'),
                    to_attr='hide_title_attrs',
                ),
            )
        )
