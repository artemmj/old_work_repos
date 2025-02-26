import pytest

from apps.template.models.template_choices import TemplateExportFieldChoices
from apps.project.tasks.export_document_services.core import ExportDocumentService
from apps.project.tasks.export_document_services.write_doc_discrepancy_field import WriteDocDiscrepancyFieldService

pytestmark = [pytest.mark.django_db]


def test_write_doc_discrepancy_field(project_for_export_document, templates_export_factory):
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
            TemplateExportFieldChoices.ZONE_NAME,
            TemplateExportFieldChoices.ZONE_NUMBER,

            TemplateExportFieldChoices.PRICE,
            TemplateExportFieldChoices.DATA_MATRIX_CODE,
            TemplateExportFieldChoices.STORE_NUMBER,
            TemplateExportFieldChoices.AM,
            TemplateExportFieldChoices.DM,
            TemplateExportFieldChoices.ZONE_CODE,
            TemplateExportFieldChoices.STORAGE_CODE,
            TemplateExportFieldChoices.REMAINDER_2,
            TemplateExportFieldChoices.SIZE,
        ]
    )
    core_service = ExportDocumentService(
        project_id=project_for_export_document.pk,
        template_id=template_export.pk,
        file_format='txt',
    )
    filepath, _ = core_service._create_db_file()
    WriteDocDiscrepancyFieldService(
        zone_number_start=1,
        zone_number_end=3,
        project=project_for_export_document,
        template=template_export,
        filepath=filepath,
    ).process()

    with open(filepath, encoding='windows-1251') as ifile:
        # 2222; Второй;      www; 20.000;  0.000;  -20;  -20.000; zone_2; 2  ...
        # 3333; Неизвестный; eee; 30.000;  35.000;  5;   5.000;   zone_3; 3  ...
        # 1111; Первый;      qqq; 10.000;  9.000;   -1;  -1.000;  zone_1; 1  ...
        lines = ifile.readlines()
        assert lines[-1].split(';')[5] == '-1'
        assert lines[-1].split(';')[6] == '-1.000'
        assert lines[-2].split(';')[5] == '5'
        assert lines[-2].split(';')[6] == '5.000'
        assert lines[-3].split(';')[5] == '-20'
        assert lines[-3].split(';')[6] == '-20.000'
