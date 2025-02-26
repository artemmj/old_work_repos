import json
import logging

import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError

from apps.helpers.services import AbstractService
from apps.transaction.services.check_value import CheckValueService

logger = logging.getLogger()


class PayRequestService(AbstractService):
    """Сервис получения URL адреса для оплаты."""

    def __init__(self, transaction):  # noqa: D107
        self.transaction = transaction

    def process(self):
        url = f'{settings.ASSIST_TEST_HOST}/pay/payrequest.cfm'
        payload = {
            'Merchant_ID': settings.ASSIST_MERCHANT_ID,
            'OrderNumber': str(self.transaction.id),
            'OrderAmount': str(self.transaction.amount),
            'ChequeItems': self._get_cheque_items(),
            'Checkvalue': CheckValueService(self.transaction).process(),
            'URL_RETURN': settings.ASSIST_URL_RETURN,
        }
        try:  # noqa: WPS229
            response = requests.post(url, data=payload, timeout=60)
            payment_url = response.json()['URL']
            self.transaction.payment_url = payment_url
            self.transaction.save()
        except Exception as error:
            logger.info(f'Ошибка при получении URL адреса для оплаты. {error}')
            raise ValidationError({'error': 'Ошибка при получении URL адреса для оплаты.'})

    def _get_cheque_items(self):
        return json.dumps({  # noqa: WPS318, E111, E117
            'items': [{  # noqa: E121
                'id': 1,
                'name': f'{self.transaction.operation.label} организации {self.transaction.organization.title}',
                'price': str(self.transaction.amount),
                'quantity': 1,
                'amount': str(self.transaction.amount),
                'tax': 'vat10',
            }],
        })  # noqa: E122
