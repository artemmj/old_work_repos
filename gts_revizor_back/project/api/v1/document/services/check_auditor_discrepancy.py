from apps.helpers.services import AbstractService
from apps.task.models import Task


class CheckAuditorDiscrepancyService(AbstractService):
    def process(self, counter_task: Task, auditor_task: Task):
        counter_products = {}
        for product in counter_task.scanned_products.all():
            counter_products[product.product.pk] = product.amount

        auditor_products = {}
        for product in auditor_task.scanned_products.all():
            auditor_products[product.product.pk] = product.amount

        for cproduct, camount in counter_products.items():
            if cproduct not in auditor_products.keys():
                return True
            else:
                if camount != auditor_products[cproduct]:  # noqa: WPS513
                    return True

        return False
