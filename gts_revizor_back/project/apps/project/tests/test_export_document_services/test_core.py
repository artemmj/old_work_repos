import pytest

from apps.event.models import Event
from apps.project.tasks.export_document_services.core import ExportDocumentService
from apps.template.models.template_choices import TemplateExportFieldChoices

pytestmark = [pytest.mark.django_db]


def test_core_export_document(project_for_export_document, templates_export_factory):
    template_export = templates_export_factory(
        count=1,
        field_separator=';',
        decimal_separator=',',
        fields=[
            TemplateExportFieldChoices.BARCODE,
            TemplateExportFieldChoices.TITLE,
            TemplateExportFieldChoices.VENDOR_CODE,
            TemplateExportFieldChoices.COUNT,
        ]
    )
    service = ExportDocumentService(
        project_id=project_for_export_document.pk,
        template_id=template_export.pk,
        file_format='txt',
    )
    file_id = service.process()
    assert file_id
    assert Event.objects.all().count() == 1
