import pytest

from apps.project.tasks.export_document_services.write_standard_doc import WriteStandardDocService
from apps.template.models.template_choices import TemplateExportFieldChoices
from apps.project.tasks.export_document_services.core import ExportDocumentService

pytestmark = [pytest.mark.django_db]


def test_write_standard_doc(project_for_export_document, templates_export_factory):
    template_export = templates_export_factory(
        count=1,
        field_separator=';',
        decimal_separator=',',
        fields=[
            TemplateExportFieldChoices.BARCODE,
            TemplateExportFieldChoices.TITLE,
            TemplateExportFieldChoices.VENDOR_CODE,
            TemplateExportFieldChoices.REMAINDER,
            TemplateExportFieldChoices.COUNT,
            TemplateExportFieldChoices.DISCREPANCY,
            TemplateExportFieldChoices.DISCREPANCY_DECIMAL,

            TemplateExportFieldChoices.PRICE,
            TemplateExportFieldChoices.DATA_MATRIX_CODE,
            TemplateExportFieldChoices.STORE_NUMBER,
            TemplateExportFieldChoices.AM,
            TemplateExportFieldChoices.DM,
            TemplateExportFieldChoices.ZONE_CODE,
            TemplateExportFieldChoices.STORAGE_CODE,
            TemplateExportFieldChoices.REMAINDER_2,
            TemplateExportFieldChoices.SIZE,
            TemplateExportFieldChoices.ZONE_NAME,
            TemplateExportFieldChoices.ZONE_NUMBER,
        ]
    )
    core_service = ExportDocumentService(
        project_id=project_for_export_document.pk,
        template_id=template_export.pk,
        file_format='txt',
    )
    filepath, _ = core_service._create_db_file()
    WriteStandardDocService(
        zone_number_start=1,
        zone_number_end=3,
        project=project_for_export_document,
        template=template_export,
        filepath=filepath,
    ).process()

    with open(filepath, encoding='windows-1251') as ifile:
        # 3333;  Неизвестный; eee;  30.000;  35;   0;     0;       500.00  ...
        # 2222;  Второй;      www;  20.000;  0;   -20;  -20.000;   500.00  ...
        # 1111;  Первый;      qqq;  10.000;  9;   -1;   -1.000;    500.00  ...
        lines = ifile.readlines()
        assert lines[-1].split(';')[5] == '-1'
        assert lines[-1].split(';')[6] == '-1.000'
        assert lines[-2].split(';')[5] == '-20'
        assert lines[-2].split(';')[6] == '-20.000'
