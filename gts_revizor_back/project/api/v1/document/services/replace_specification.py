from django.db import transaction

from api.v1.document.services.change_document_status_to_ready import ChangeDocumentStatusToReady
from apps.document.models import Document, DocumentColorChoices, DocumentStatusChoices
from apps.helpers.services import AbstractService
from apps.product.models import ScannedProduct
from apps.task.models import Task
from apps.zone.models import ZoneStatusChoices


class ReplaceDocumentSpecificationService(AbstractService):

    def process(self, source: str, document: Document):
        """Заменяет спецификацию у Счётчика.

        https://git.your-site.pro/gts_revizor/gts_revizor_back/-/issues/299

        Args:
            source: источник спецификации (Аудитор (auditor) или Внешний Аудитор(auditor_external))
            document: документ, в котором будет заменяться спецификация у Счётчика

        Returns:
            document: документ с новой спецификацией у Счётчика
        """
        with transaction.atomic():
            source_task_mapping = {
                'auditor': document.auditor_task,
                'auditor_external': document.auditor_external_task,
            }

            current_auditor_task = source_task_mapping.get(source)
            if current_auditor_task is None:
                return None

            current_counter_task = document.counter_scan_task
            new_counter_task = Task.objects.create(
                zone=current_counter_task.zone,
                employee=current_counter_task.employee,
                type=current_counter_task.type,
                status=current_counter_task.status,
                result=current_auditor_task.result,
                terminal=current_counter_task.terminal,
            )
            current_scanned_products = ScannedProduct.objects.filter(task=current_auditor_task)
            ScannedProduct.objects.bulk_create(
                [
                    ScannedProduct(
                        product=current_scanned_product.product,
                        task=new_counter_task,
                        amount=current_scanned_product.amount,
                        scanned_time=current_scanned_product.scanned_time,
                        added_by_product_code=current_scanned_product.added_by_product_code,
                        is_weight=current_scanned_product.is_weight,
                        dm=current_scanned_product.dm,
                    )
                    for current_scanned_product in current_scanned_products
                ],
            )
            document.counter_scan_task = new_counter_task

            if document.status == DocumentStatusChoices.NOT_READY:
                ChangeDocumentStatusToReady(document).process()

            document.is_replace_specification = True
            document.save()

        return document
