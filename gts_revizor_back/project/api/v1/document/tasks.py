from typing import List

from api.v1.document.services import DocumentBatchDiscrepancyReportsService, DocumentDiscrepancyReportService
from apps import app


@app.task
def generate_discrepancy_report_task(document_id, endpoint_prefix):
    return DocumentDiscrepancyReportService(document_id, endpoint_prefix).process()


@app.task
def generate_batch_discrepancy_report_task(endpoint_prefix: str, document_ids: List[int]):
    return DocumentBatchDiscrepancyReportsService(endpoint_prefix, document_ids).process()
