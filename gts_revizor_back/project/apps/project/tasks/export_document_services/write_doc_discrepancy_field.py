import csv
from typing import Dict

from apps.document.models import Document, DocumentStatusChoices
from apps.helpers.services import AbstractService
from apps.product.models import Product
from apps.project.models.project import Project
from apps.project.tasks.export_document_services.add_title_attrs import AddTitleAttrsService
from apps.template.models import TemplateExport
from apps.template.models.template_choices import TemplateExportFieldChoices


class WriteDocDiscrepancyFieldService(AbstractService):
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
        Если есть поле Расхождение или Расхождение с десятичной
        частью - смотреть все товары и считать разницу от отсканировнных.
        """
        with open(self.filepath, 'w', encoding='windows-1251') as ifile:
            self.writer = csv.writer(ifile, delimiter=self.template.field_separator)
            source_data = {}
            for product in Product.objects.filter(project=self.project, remainder__isnull=False):
                source_data[product] = self._collect_product_data(product)

            self._collect_scanned_data(source_data)
            self._write_source_data_in_file(source_data)

    def _collect_product_data(self, product: Product):
        """Ф_ция собирает данные по товару, собирает доп. аттрибуты."""
        data = {
            'barcode': product.barcode if not any(   # noqa: WPS504
                [self.template.is_products_find_by_code, self.template.is_products_find_by_qr_code],
            ) else '',
            'vendor_code': product.vendor_code,
            'qr_code': product.qr_code,
            'title': product.title,
            'price': float(product.price),
            'remainder': product.remainder,
            'store_number': product.store_number,
            'size': product.size,
            'remainder_2': product.remainder_2,
            'count': 0,
            'discrepancy': None,
            'discrepancy_decimal': None,
        }
        return AddTitleAttrsService().process(
            export_content=data, product_id=product.id, project_id=self.project.id,
        )

    def _collect_scanned_data(self, source_data: Dict):   # noqa: WPS231
        """Ф_ция собирает к сырым данным инфу по сканированию каждого товара."""
        project_documents = Document.objects.filter(
            status=DocumentStatusChoices.READY,
            zone__project=self.project,
            zone__serial_number__gte=self.zone_number_start,
            zone__serial_number__lte=self.zone_number_end,
        )
        if self.template.storage_name:
            project_documents = project_documents.filter(zone__storage_name=self.template.storage_name)
        for document in project_documents:
            scanned_products = document.counter_scan_task.scanned_products.all()
            if self.template.is_products_find_by_code:
                scanned_products = document.counter_scan_task.scanned_products.filter(added_by_product_code=True)
            if self.template.is_products_find_by_qr_code:
                scanned_products = document.counter_scan_task.scanned_products.filter(added_by_qr_code=True)
            for scanned_product in scanned_products:
                source_data[scanned_product.product]['zone_name'] = document.zone.title
                source_data[scanned_product.product]['zone_number'] = document.zone.serial_number
                source_data[scanned_product.product]['storage_code'] = document.zone.storage_name
                source_data[scanned_product.product]['count'] += scanned_product.amount
                source_data[scanned_product.product]['zone_code'] = document.zone.code
                source_data[scanned_product.product]['am'] = scanned_product.product.am
                source_data[scanned_product.product]['dm'] = scanned_product.product.dm
                source_data[scanned_product.product]['data_matrix_code'] = scanned_product.product.dm
                source_data[scanned_product.product]['terminal'] = document.tsd_number
                if getattr(scanned_product, 'dm', False) and scanned_product.dm:
                    source_data[scanned_product.product]['dm'] = scanned_product.dm
                    source_data[scanned_product.product]['data_matrix_code'] = scanned_product.dm

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

    def _write_source_data_in_file(self, source_data: Dict):
        for product in source_data.keys():
            product = self._check_fields(source_data[product])
            row_data = []
            if product['discrepancy'] == 0 or product['discrepancy_decimal'] == 0:
                continue
            for key in self.template.fields:
                row_data.append(f'{product[key]}')
            self.writer.writerow(row_data)
