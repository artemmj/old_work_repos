import logging
from datetime import datetime
from decimal import Decimal
from secrets import token_urlsafe

from django.conf import settings
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from api.v1.reports.services.helpers.check_reports_directory import check_reports_directory
from apps.document.models import Document
from apps.helpers.services import AbstractService

logger = logging.getLogger('django')


class DocumentDiscrepancyReportService(AbstractService):

    def __init__(self, document_id, endpoint_prefix, is_output_dest: bool = False) -> None:
        self.document = Document.objects.get(pk=document_id)
        self.endpoint_pref = endpoint_prefix
        self.is_output_dest = is_output_dest

    def process(self, *args, **kwargs):
        context = self._create_context_for_report()
        res = render_to_string('document/discrepancy.html', context)
        date = check_reports_directory()
        filename = f'discrepancy-report_{token_urlsafe(5)}.pdf'
        output_dest = f'{settings.MEDIA_ROOT}/reports/{date}/{filename}'

        with open(output_dest, 'wb+') as ofile:
            pisa.CreatePDF(res, ofile)

        if self.is_output_dest:
            return output_dest
        return f'{self.endpoint_pref}/media/reports/{date}/{filename}'

    def _create_context_for_report(self):  # noqa: WPS231
        """Наполнить контекст для рендера html страницы."""
        result = {}
        if self.document.counter_scan_task:
            for prd in self.document.counter_scan_task.scanned_products.all():
                product_id = str(prd.product.pk)
                if product_id not in result:
                    result[product_id] = {}  # noqa: WPS204
                result[product_id]['cresult'] = prd.amount
                result[product_id]['barcode'] = prd.product.barcode
                result[product_id]['title'] = prd.product.title

        if self.document.auditor_task:
            for prd in self.document.auditor_task.scanned_products.all():
                product_id = str(prd.product.pk)
                if product_id not in result:
                    result[product_id] = {}
                result[product_id]['aresult'] = prd.amount
                result[product_id]['barcode'] = prd.product.barcode
                result[product_id]['title'] = prd.product.title

        if self.document.auditor_external_task:
            for prd in self.document.auditor_external_task.scanned_products.all():
                product_id = str(prd.product.pk)
                if product_id not in result:
                    result[product_id] = {}
                result[product_id]['aeresult'] = prd.amount
                result[product_id]['barcode'] = prd.product.barcode
                result[product_id]['title'] = prd.product.title

        for key in result.keys():
            if 'cresult' not in result[key]:  # noqa: WPS204
                result[key]['cresult'] = Decimal('0.000')
            if 'aresult' not in result[key]:
                result[key]['aresult'] = Decimal('0.000')
            if 'aeresult' not in result[key]:
                result[key]['aeresult'] = Decimal('0.000')

            if (  # noqa: WPS502 WPS337
                result[key]['aresult'] and (result[key]['cresult'] != result[key]['aresult'])
                or result[key]['aeresult'] and (result[key]['cresult'] != result[key]['aeresult'])
            ):
                result[key]['discrepancy'] = True
            else:
                result[key]['discrepancy'] = False

        context_list_prds = []
        for item in result.values():
            context_list_prds.append({
                'barcode': item['barcode'],
                'title': item['title'],
                'cresult': item['cresult'],
                'aresult': item['aresult'],
                'ext_auditor': item['aeresult'],
                'discrepancy': '*' if item['discrepancy'] else ' ',
            })

        context = {
            'project': self.document.zone.project.title,
            'curr_date': datetime.today(),
            'zone': self.document.zone.title,
            'scanned_products': context_list_prds,
        }
        return context  # noqa: WPS331
