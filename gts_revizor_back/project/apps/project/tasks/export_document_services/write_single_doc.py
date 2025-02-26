import csv
import logging
from typing import Dict, List

from apps.document.models import Document, DocumentStatusChoices
from apps.helpers.services import AbstractService
from apps.project.models.project import Project
from apps.project.tasks.export_document_services.add_title_attrs import AddTitleAttrsService
from apps.template.models import TemplateExport
from apps.template.models.template_choices import TemplateExportFieldChoices

logger = logging.getLogger('django')


class WriteSingleDocService(AbstractService):
    def __init__(  # noqa: WPS211
        self,
        zone_number_start: int,
        zone_number_end: int,
        project: Project,
        template: TemplateExport,
        filepath: str,
    ):
        self.zone_number_start = zone_number_start
        self.zone_number_end = zone_number_end
        self.project = project
        self.template = template
        self.filepath = filepath

    def process(self, *args, **kwargs):
        """
        Поединичная выгрузка - каждая строка это один отсканированный товар,
        строк с товаром столько, сколько его насканировали.
        """
        with open(self.filepath, 'w', encoding='windows-1251') as ifile:
            self.writer = csv.writer(ifile, delimiter=self.template.field_separator)
            source_data = self._collect_source_data()
            for product in source_data:
                product = self._check_fields(product)
                row_data = []
                if product['discrepancy'] == 0 or product['discrepancy_decimal'] == 0:
                    continue
                for key in self.template.fields:
                    row_data.append(f'{product[key]}')
                self.writer.writerow(row_data)

    def _collect_source_data(self) -> List:   # noqa: WPS231
        project_documents = Document.objects.filter(
            status=DocumentStatusChoices.READY,
            zone__project=self.project,
            zone__serial_number__gte=self.zone_number_start,
            zone__serial_number__lte=self.zone_number_end,
        )
        if self.template.storage_name:
            project_documents = project_documents.filter(zone__storage_name=self.template.storage_name)

        source_data = []
        for document in project_documents:
            scanned_products = document.counter_scan_task.scanned_products.all()
            if self.template.is_products_find_by_code:
                scanned_products = document.counter_scan_task.scanned_products.filter(added_by_product_code=True)
            if self.template.is_products_find_by_qr_code:
                scanned_products = document.counter_scan_task.scanned_products.filter(added_by_qr_code=True)
            for scanned in scanned_products:
                data = {
                    'barcode': scanned.product.barcode if not any(   # noqa: WPS504
                        [self.template.is_products_find_by_code, self.template.is_products_find_by_qr_code],
                    ) else '',
                    'vendor_code': scanned.product.vendor_code,
                    'qr_code': scanned.product.qr_code,
                    'title': scanned.product.title,
                    'price': float(scanned.product.price),
                    'remainder': scanned.product.remainder,
                    'store_number': scanned.product.store_number,
                    'size': scanned.product.size,
                    'remainder_2': scanned.product.remainder_2,
                    'count': scanned.amount,
                    'discrepancy': None,
                    'discrepancy_decimal': None,
                    'data_matrix_code': None,
                    'am': scanned.product.am,
                    'dm': scanned.dm if getattr(scanned, 'dm', False) else scanned.product.dm,
                    'zone_name': document.zone.title,
                    'zone_code': document.zone.code,
                    'storage_code': document.zone.storage_name,
                    'terminal': document.tsd_number,
                }
                data = AddTitleAttrsService().process(
                    export_content=data, product_id=scanned.product.id, project_id=self.project.id,
                )
                for _i in range(int(scanned.amount)):  # noqa: WPS122
                    source_data.append(data)

        return source_data

    def _check_fields(self, product: Dict) -> Dict:
        if 'zone_name' not in product:
            product['zone_name'] = None
        if 'zone_number' not in product:
            product['zone_number'] = None
        if 'storage_code' not in product:
            product['storage_code'] = None
        if TemplateExportFieldChoices.DISCREPANCY in self.template.fields:
            product['discrepancy'] = int(product['count'] - product['remainder'])
            if product['remainder'] < 0:
                product['discrepancy'] = int(abs(product['remainder'] - product['count']))
        if TemplateExportFieldChoices.DISCREPANCY_DECIMAL in self.template.fields:
            product['discrepancy_decimal'] = product['count'] - product['remainder']
            if product['remainder'] < 0:
                product['discrepancy_decimal'] = abs(product['remainder'] - product['count'])
        return product
