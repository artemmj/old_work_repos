import pytest

from apps.template.models.template_choices import TemplateExportFieldChoices
from apps.project.tasks.export_document_services.core import ExportDocumentService
from apps.project.tasks.export_document_services.write_single_doc import WriteSingleDocService

pytestmark = [pytest.mark.django_db]


def test_write_single_doc_zone_first(project_for_export_doc_zone_first, templates_export_factory):
    template_export = templates_export_factory(
        count=1,
        field_separator=';',
        decimal_separator=',',
        fields=[
            TemplateExportFieldChoices.ZONE_NAME,
            TemplateExportFieldChoices.ZONE_CODE,
            TemplateExportFieldChoices.STORAGE_CODE,
            TemplateExportFieldChoices.BARCODE,
            TemplateExportFieldChoices.TITLE,
            TemplateExportFieldChoices.VENDOR_CODE,
            TemplateExportFieldChoices.REMAINDER,
            TemplateExportFieldChoices.COUNT,
            TemplateExportFieldChoices.DISCREPANCY,
            TemplateExportFieldChoices.DISCREPANCY_DECIMAL,
            TemplateExportFieldChoices.ZONE_NUMBER,

            TemplateExportFieldChoices.PRICE,
            TemplateExportFieldChoices.DATA_MATRIX_CODE,
            TemplateExportFieldChoices.STORE_NUMBER,
            TemplateExportFieldChoices.AM,
            TemplateExportFieldChoices.DM,
            TemplateExportFieldChoices.REMAINDER_2,
            TemplateExportFieldChoices.SIZE,
        ]
    )
    core_service = ExportDocumentService(
        project_id=project_for_export_doc_zone_first.pk,
        template_id=template_export.pk,
        file_format='txt',
    )
    filepath, _ = core_service._create_db_file()
    WriteSingleDocService(
        zone_number_start=1,
        zone_number_end=3,
        project=project_for_export_doc_zone_first,
        template=template_export,
        filepath=filepath,
    ).process()

    with open(filepath, encoding='windows-1251') as ifile:
        lines = ifile.readlines()
        assert lines[0].split(';')[0] == 'zone_3'
        assert lines[0].split(';')[1] == 'code3'
        assert lines[0].split(';')[2] == 'storage3'
