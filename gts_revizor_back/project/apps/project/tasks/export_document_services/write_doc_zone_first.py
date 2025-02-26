import csv
from typing import Dict

from apps.document.models import Document, DocumentStatusChoices
from apps.helpers.services import AbstractService
from apps.product.models import ScannedProduct
from apps.project.models.project import Project
from apps.project.tasks.export_document_services.add_title_attrs import AddTitleAttrsService
from apps.template.models import TemplateExport
from apps.template.models.template_choices import TemplateExportFieldChoices


class WriteDocZoneFirstService(AbstractService):
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
        """Если в шаблоне первое поле Название зоны или Код/номер зоны - алгоритм агрегации данных отличается."""
        with open(self.filepath, 'w', encoding='windows-1251') as ifile:
            writer = csv.writer(ifile, delimiter=self.template.field_separator)

            source_data = []
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
                for scanned in scanned_products:
                    product_data = self._collect_product_data(scanned, document)
                    self._check_fields(product_data, scanned)
                    source_data.append(product_data)

            sorted_data = sorted(source_data, key=lambda x: x['zone_number'])

            row_data = []
            for product_data in sorted_data:
                for key in self.template.fields:
                    row_data.append(f'{product_data[key]}')
                writer.writerow(row_data)
                row_data.clear()

    def _collect_product_data(self, scanned_p: ScannedProduct, document: Document) -> Dict:
        """Ф_ция собирает данные по товару, собирает доп. аттрибуты."""
        # Если товар весовой, количество в нем это вес в граммах, отобразить по разрядам через запятую
        count = int(scanned_p.amount)
        if scanned_p.is_weight:
            count = '{0:}'.format(scanned_p.amount).replace('.', ',')
        data = {
            'zone_name': document.zone.title,
            'zone_number': document.zone.serial_number,
            'storage_code': document.zone.storage_name,
            'barcode': scanned_p.product.barcode if not any(   # noqa: WPS504
                [self.template.is_products_find_by_code, self.template.is_products_find_by_qr_code],
            ) else '',
            'vendor_code': scanned_p.product.vendor_code,
            'title': scanned_p.product.title,
            'price': float(scanned_p.product.price),
            'data_matrix_code': scanned_p.dm,
            'size': scanned_p.product.size,
            'count': count,
            'remainder': scanned_p.product.remainder,
            'store_number': scanned_p.product.store_number,
            'remainder_2': scanned_p.product.remainder_2,
            'am': scanned_p.product.am,
            'dm': scanned_p.dm if getattr(scanned_p, 'dm', False) else scanned_p.product.dm,
            'zone_code': document.zone.code,
            'terminal': document.tsd_number,
            'qr_code': scanned_p.product.qr_code,
        }
        return AddTitleAttrsService().process(
            export_content=data, product_id=scanned_p.product.id, project_id=self.project.id,
        )

    def _check_fields(self, product_data: Dict, scanned: ScannedProduct) -> Dict:
        if TemplateExportFieldChoices.DISCREPANCY in self.template.fields:
            discrepancy = int(scanned.amount - scanned.product.remainder)
            if scanned.product.remainder < 0:
                discrepancy = int(abs(scanned.product.remainder - scanned.amount))
            product_data['discrepancy'] = discrepancy
        if TemplateExportFieldChoices.DISCREPANCY_DECIMAL in self.template.fields:
            discrepancy = scanned.amount - scanned.product.remainder
            if scanned.product.remainder < 0:
                discrepancy = abs(scanned.product.remainder - scanned.amount)
            product_data['discrepancy_decimal'] = discrepancy
