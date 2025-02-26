from decimal import Decimal
from typing import Dict

from django.db.models import Sum

from apps.document.models import Document, DocumentStatusChoices
from apps.helpers.services import AbstractService
from apps.product.models import Product
from apps.project.models import Project
from apps.zone.models import Zone, ZoneStatusChoices


class ProjectStatisticService(AbstractService):
    def __init__(self, instance: Project) -> None:
        self.instance = instance

    def process(self) -> Dict:
        project_products = Product.objects.filter(project=self.instance)
        project_zones = Zone.objects.filter(project=self.instance)
        project_ready_zones = project_zones.filter(status=ZoneStatusChoices.READY)

        prdocuments = Document.objects.filter(zone__project=self.instance, status=DocumentStatusChoices.READY)
        counted_tmc = prdocuments.aggregate(
            counted_tmc=Sum('counter_scan_task__scanned_products__amount'),
        )['counted_tmc']
        fdocument = Document.objects.filter(zone__project=self.instance).order_by('created_at').first()
        ldocument = Document.objects.filter(zone__project=self.instance).order_by('created_at').last()

        account_qs_balance = project_products.aggregate(Sum('remainder'))['remainder__sum'] or 0

        counted_tmc_percent = 0
        counted_zones_percent = 0
        if account_qs_balance and counted_tmc:
            counted_tmc_percent = round(Decimal(counted_tmc) / Decimal(account_qs_balance) * 100, 0)
        if project_zones.count():
            counted_zones_percent = round(
                Decimal(project_ready_zones.count()) / Decimal(project_zones.count()) * 100, 0,
            )

        scan_begin = None
        if fdocument and getattr(fdocument, 'start_audit_date', False):
            scan_begin = fdocument.start_audit_date.strftime('%Y-%m-%dT%H:%M')

        scan_end = None
        if ldocument and getattr(ldocument, 'end_audit_date', False):
            scan_end = fdocument.end_audit_date.strftime('%Y-%m-%dT%H:%M')

        scan_begin = None
        if fdocument and getattr(fdocument, 'start_audit_date', False):
            scan_begin = fdocument.start_audit_date.strftime('%Y-%m-%dT%H:%M')

        scan_end = None
        if ldocument and getattr(ldocument, 'end_audit_date', False):
            scan_end = fdocument.end_audit_date.strftime('%Y-%m-%dT%H:%M')

        statistic = {
            'product_count': project_products.distinct('title').order_by().count(),
            'barcode_count': project_products.count(),
            'zone_count': project_zones.count(),
            'account_balance': account_qs_balance,
            'scan_begin': scan_begin,
            'scan_end': scan_end,
            'counted_tmc': {
                'alls_tmc': account_qs_balance,
                'scanned_tmc': counted_tmc,
                'percent': counted_tmc_percent,
            },
            'counted_zones': {
                'all_zones': project_zones.count(),
                'ready_zones': project_ready_zones.count(),
                'percent': counted_zones_percent,
            },
        }
        return statistic  # noqa: WPS331
