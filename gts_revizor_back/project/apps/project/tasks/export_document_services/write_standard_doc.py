import csv
from typing import Dict

from apps.document.models import Document, DocumentStatusChoices
from apps.helpers.services import AbstractService
from apps.project.models.project import Project
from apps.project.tasks.export_document_services.add_title_attrs import AddTitleAttrsService
from apps.template.models import TemplateExport
from apps.template.models.template_choices import TemplateExportFieldChoices


class WriteStandardDocService(AbstractService):
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
        """Стандартная отработака сборки документа, по всем готовым докам (напр. первое поле шк или код товара)."""
        with open(self.filepath, 'w', encoding='windows-1251') as ifile:
            writer = csv.writer(ifile, delimiter=self.template.field_separator)
            source_data = self._collect_source_data()
            source_data = self._check_discrepancy_field(source_data)

            doc_dict, row_data = {}, []
            for product_data in source_data.values():
                count = int(product_data['count'])
                if product_data['is_weight']:
                    # Если товар весовой, количество в нем это вес в граммах, отобразить по разрядам через запятую
                    count = '{0:}'.format(product_data['count']).replace('.', ',')
                product_data['count'] = count

                doc_dict = AddTitleAttrsService().process(
                    export_content=product_data, product_id=product_data['id'], project_id=self.project.id,
                )

                if TemplateExportFieldChoices.DISCREPANCY in product_data:
                    doc_dict['discrepancy'] = int(product_data['discrepancy'])
                if TemplateExportFieldChoices.DISCREPANCY_DECIMAL in product_data:
                    doc_dict['discrepancy_decimal'] = product_data['discrepancy_decimal']

                for key in self.template.fields:
                    row_data.append(f'{doc_dict[key]}')

                writer.writerow(row_data)

                doc_dict.clear()
                row_data.clear()

    def _collect_source_data(self) -> Dict:  # noqa: WPS231
        source_data = {}

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
                uniq_id = scanned.dm if scanned.dm else scanned.product.barcode

                if uniq_id not in source_data:
                    source_data[uniq_id] = {
                        'id': scanned.product.id,
                        'zone_name': document.zone.title,
                        'zone_number': document.zone.serial_number,
                        'zone_code': document.zone.code,
                        'storage_code': document.zone.storage_name,
                        'barcode': scanned.product.barcode if not any(  # noqa: WPS504
                            [self.template.is_products_find_by_code, self.template.is_products_find_by_qr_code],
                        ) else '',
                        'vendor_code': scanned.product.vendor_code,
                        'title': scanned.product.title,
                        'price': scanned.product.price,
                        'data_matrix_code': scanned.dm,
                        'count': scanned.amount,
                        'size': scanned.product.size,
                        'is_weight': scanned.is_weight,
                        'remainder': scanned.product.remainder,
                        'store_number': scanned.product.store_number,
                        'remainder_2': scanned.product.remainder_2,
                        'discrepancy': 0,
                        'discrepancy_decimal': 0,
                        'am': scanned.product.am,
                        'dm': scanned.dm if getattr(scanned, 'dm', False) else scanned.product.dm,
                        'terminal': document.tsd_number,
                        'qr_code': scanned.product.qr_code,
                    }
                else:
                    source_data[uniq_id]['count'] += scanned.amount

        return source_data

    def _check_discrepancy_field(self, source_data: Dict) -> Dict:  # noqa: WPS231
        discrep_in_template = TemplateExportFieldChoices.DISCREPANCY in self.template.fields
        discrep_decimal_in_template = TemplateExportFieldChoices.DISCREPANCY_DECIMAL in self.template.fields

        if discrep_in_template or discrep_decimal_in_template:
            for product_id in source_data.keys():
                if source_data[product_id]['count'] == source_data[product_id]['remainder']:
                    continue
                if discrep_in_template:
                    source_data[product_id] = self._set_discrepancy(source_data[product_id])
                if discrep_decimal_in_template:
                    source_data[product_id] = self._set_decimal_discrepancy(source_data[product_id])

        return source_data

    def _set_discrepancy(self, product: Dict) -> Dict:
        product['discrepancy'] = int(product['count'] - product['remainder'])
        if product['remainder'] < 0:
            product['discrepancy'] = int(abs(product['remainder'] - product['count']))
        return product

    def _set_decimal_discrepancy(self, product: Dict) -> Dict:
        product['discrepancy_decimal'] = product['count'] - product['remainder']
        if product['remainder'] < 0:
            product['discrepancy_decimal'] = abs(product['remainder'] - product['count'])
        return product
