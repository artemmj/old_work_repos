from secrets import token_urlsafe
from typing import List

from django.conf import settings

from api.v1.document import services as doc_services
from api.v1.reports.services.helpers.check_reports_directory import check_reports_directory
from apps.document.models import Document, DocumentStatusChoices
from apps.helpers.pdf_files import merge_pdf_files
from apps.helpers.services import AbstractService


class DocumentBatchDiscrepancyReportsService(AbstractService):
    """Сервис генерации отчёта по расхождениям для списка документов."""

    def __init__(self, endpoint_prefix: str, document_ids: List[int]) -> None:
        self.endpoint_prefix = endpoint_prefix
        self.document_ids = document_ids

    def process(self, *args, **kwargs):
        filename = f'discrepancy-report_{token_urlsafe(5)}.pdf'
        generation_date = check_reports_directory()
        output_dest = f'{settings.MEDIA_ROOT}/reports/{generation_date}/{filename}'
        date = check_reports_directory()

        documents = Document.objects.filter(pk__in=self.document_ids).order_by('zone__serial_number')
        paths_to_generated_reports = self._generate_discrepancy_report_for(documents=documents)

        merge_pdf_files(paths_to_generated_reports, output_dest)

        return f'{self.endpoint_prefix}/media/reports/{date}/{filename}'

    def _generate_discrepancy_report_for(self, documents: List[Document]):  # noqa: WPS231
        paths_to_generated_reports = []

        for document in documents:
            if document.auditor_task is None:
                continue

            if document.status == DocumentStatusChoices.NOT_READY:
                continue

            is_discrepancy = doc_services.CheckAuditorDiscrepancyService().process(
                counter_task=document.counter_scan_task,
                auditor_task=document.auditor_task,
            )
            if not is_discrepancy:
                continue

            path_to_discrepancy_report_file = doc_services.DocumentDiscrepancyReportService(
                document_id=document.id,
                endpoint_prefix=self.endpoint_prefix,
                is_output_dest=True,
            ).process()

            paths_to_generated_reports.append(path_to_discrepancy_report_file)

        return paths_to_generated_reports
