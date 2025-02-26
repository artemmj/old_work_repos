import logging
import os
from dataclasses import dataclass
from secrets import token_urlsafe

import polars as pl
from django.utils import timezone

from apps import app
from apps.document.models import DocumentStatusChoices
from apps.file.models import File
from apps.helpers.services import AbstractService
from apps.product.models import ScannedProduct
from apps.project.models import Project
from apps.project.services.get_scanned_products_attrs import GetScannedProductsAttrsService
from apps.template.models import TemplateExport, TemplateExportFieldChoices

logger = logging.getLogger('django')


@app.task
def export_document_celery_wrapper(project_id: str, template_id: str, export_file_format: str):  # noqa: WPS125
    """Асинхронная обертка для сервиса."""
    return ExportDocumentService(
        project_id=project_id,
        template_id=template_id,
        export_file_format=export_file_format,
    ).process()


@dataclass
class ExportFile:
    filepath: str
    file_object: File


class ExportDocumentService(AbstractService):

    def __init__(self, project_id: str, template_id: str, export_file_format: str):
        self.project = Project.objects.get(pk=project_id)
        self.template = TemplateExport.objects.get(pk=template_id)
        self.export_file_format = export_file_format

    def process(self, *args, **kwargs):
        export_content = self._prepare_content_for_export()
        documents_df = self._add_export_content_to_df(export_content=export_content)

        export_file_with_utf_encoding = self._create_db_file()
        export_file_with_windows_encoding = self._create_db_file()

        self._save_dataframe_with_export_content_to_csv(
            df=documents_df,
            filepath=export_file_with_utf_encoding.filepath,
            field_separator=self.template.field_separator,
        )

        self._change_encoding_in_csv_from_utf_to_windows(
            filepath_with_utf_encoding=export_file_with_utf_encoding.filepath,
            filepath_with_windows_encoding=export_file_with_windows_encoding.filepath,
        )

        return export_file_with_windows_encoding.file_object.id

    def _prepare_content_for_export(self):
        scanned_products = (
            ScannedProduct
            .objects
            .filter(
                task__counter_scan_document__status=DocumentStatusChoices.READY,
                task__counter_scan_document__zone__project=self.project,
            )
            .with_discrepancy_calculation()
            .order_by('product__barcode')
        )

        if self.template.storage_name:
            scanned_products = scanned_products.filter(
                task__counter_scan_document__zone__storage_name=self.template.storage_name,
            )

        scanned_products_attrs = GetScannedProductsAttrsService(scanned_products).process()

        return {
            'title': scanned_products_attrs.titles,
            'barcode': scanned_products_attrs.barcodes,
            'count': scanned_products_attrs.amounts,
            'zone_name': scanned_products_attrs.zones_names,
            'zone_code': scanned_products_attrs.zones_codes,
            'zone_number': scanned_products_attrs.zones_numbers,
            'vendor_code': scanned_products_attrs.vendor_codes,
            'price': scanned_products_attrs.prices,
            'data_matrix_code': scanned_products_attrs.dm_codes,
            'count_scanned_product': scanned_products_attrs.amounts,
            'counter_code': scanned_products_attrs.documents_counter_codes,
            'store_number': scanned_products_attrs.store_numbers,
            'remainder': scanned_products_attrs.remainders,
            'discrepancy': scanned_products_attrs.discrepancies,
            'discrepancy_decimal': scanned_products_attrs.decimal_discrepancies,
            'is_weight': scanned_products_attrs.is_weight,
        }

    def _add_export_content_to_df(self, export_content):
        is_discrepancy_field = TemplateExportFieldChoices.DISCREPANCY in self.template.fields
        is_discrepancy_decimal_field = TemplateExportFieldChoices.DISCREPANCY_DECIMAL in self.template.fields
        is_zone_name_field = TemplateExportFieldChoices.ZONE_NAME in self.template.fields
        is_zone_number_field = TemplateExportFieldChoices.ZONE_NUMBER in self.template.fields

        if any([is_discrepancy_field, is_discrepancy_decimal_field, is_zone_name_field, is_zone_number_field]):
            return (
                pl.DataFrame(export_content)
                .with_columns(pl.col(pl.Decimal).cast(pl.Float32))
                .with_columns(
                    pl.when(pl.col('is_weight') == 1)
                    .then(pl.col('count').cast(pl.String))
                    .otherwise(pl.col('count').cast(pl.Float32).cast(pl.Int32))  # noqa: C812
                )
                .select(self.template.fields)
            )

        return (
            pl.DataFrame(export_content)
            .group_by(by='barcode')
            .agg(
                pl.col('count').sum(),
                pl.col('count_scanned_product').sum(),
                pl.col('title').first().alias('title'),
                pl.col('zone_name').first().alias('zone_name'),
                pl.col('zone_code').first().alias('zone_code'),
                pl.col('zone_number').first().alias('zone_number'),
                pl.col('vendor_code').first().alias('vendor_code'),
                pl.col('price').first().alias('price'),
                pl.col('data_matrix_code').first().alias('data_matrix_code'),
                pl.col('counter_code').first().alias('counter_code'),
                pl.col('store_number').first().alias('store_number'),
                pl.col('remainder').first().alias('remainder'),
                pl.col('discrepancy').first().alias('discrepancy'),
                pl.col('discrepancy_decimal').first().alias('discrepancy_decimal'),
                pl.col('is_weight').first().alias('is_weight'),
            )
            .with_columns(pl.col(pl.Decimal).cast(pl.Float64))
            .with_columns(
                pl.when(pl.col('is_weight') == 1)
                .then(pl.col('count').cast(pl.String))
                .otherwise(pl.col('count').cast(pl.Float32).cast(pl.Int32))  # noqa: C812
            )
            .select(self.template.fields)
        )

    def _create_db_file(self) -> ExportFile:
        now_date = timezone.now().strftime('%Y/%m/%d')

        export_dir = f'/media/upload/{now_date}/'
        os.makedirs(export_dir, exist_ok=True)

        project_title = self.project.title.replace('/', '_')
        filepath = f'{export_dir}export_document_{project_title}_{token_urlsafe(4)}.{self.export_file_format}'
        export_file = File.objects.create(file=filepath.replace('/media', ''))

        return ExportFile(filepath=filepath, file_object=export_file)

    @staticmethod
    def _save_dataframe_with_export_content_to_csv(df: pl.DataFrame, filepath: str, field_separator: str):
        df.write_csv(filepath, separator=field_separator, include_bom=True)

    @staticmethod
    def _change_encoding_in_csv_from_utf_to_windows(
        filepath_with_utf_encoding: str,
        filepath_with_windows_encoding: str,
    ):
        with open(filepath_with_utf_encoding, 'r', encoding='utf-8') as input_file:
            with open(filepath_with_windows_encoding, 'w', encoding='windows-1251') as output_file:
                output_file.write(input_file.read())
