import logging

import requests

import settings
from apps import app
from apps.transaction.models import OrganizationTransaction, OrganizationTransactionOperations
from apps.transaction.models.abstract import TransactionStatuses, TransactionTypes
from apps.transaction.services.check_value import CheckValueService
from apps.transaction.services.executor import TransactionExecutor

logger = logging.getLogger()


@app.task
def check_balance_replenishment_status():  # noqa: WPS210, WPS231
    """
    Проверка статуса транзакций на пополнение баланса
    организации в системе АПК Assist и выполнение
    транзакции на основе полученного статуса.
    """  # noqa: D205, D400
    transactions = OrganizationTransaction.objects.filter(
        type=TransactionTypes.ADD,
        operation=OrganizationTransactionOperations.BALANCE_REPLENISHMENT,
        status=TransactionStatuses.PENDING,
    )
    payload = {
        'Merchant_ID': settings.ASSIST_MERCHANT_ID,
        'Login': settings.ASSIST_LOGIN,
        'Password': settings.ASSIST_PASSWORD,
        'Format': settings.ASSIST_FORMAT,
    }
    for t in transactions:
        payload['OrderNumber'] = str(t.id)
        url = f'{settings.ASSIST_TEST_HOST}/orderstate/orderstate.cfm'
        try:
            response = requests.post(url, data=payload, timeout=60)
        except Exception as error:
            logger.info(f'Ошибка при получении статуса транзакции id={t.id}. {error}')
            continue
        if response and response.json().get('orderstate'):
            order_state = response.json()['orderstate']['orderstate']
            order_number = response.json()['orderstate']['ordernumber']
            check_value = response.json()['orderstate']['checkdata']['checkvalue']
            gen_check_value = CheckValueService(t, order_state).process()
            if order_number == str(t.id) and check_value == gen_check_value:
                if order_state in settings.ASSIST_SUCCESS_STATUSES:
                    TransactionExecutor().execute(t.id)
                    logger.info(f'Транзакция оплачена. {response.json()}.')
                if order_state in settings.ASSIST_ERROR_STATUSES:
                    t.status = TransactionStatuses.ERROR
                    t.save()
                    logger.info(f'Транзакция не оплачена. {response.json()}.')
