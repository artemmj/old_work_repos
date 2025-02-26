from typing import Union

from django.db import transaction as db_transaction
from django.db.models import F  # noqa: WPS347

from apps.inspector.models import Inspector
from apps.organization.models import Organization
from apps.transaction.models import InspectorTransaction, OrganizationTransaction
from apps.transaction.models.abstract import TransactionStatuses, TransactionTypes


class TransactionExecutor:

    @db_transaction.atomic
    def execute(self, transaction_id: str) -> bool:
        """Выполняет транзакцию.

        Если транзакция не выполнена, ей присваивается статус ошибки.

        :param transaction_id: id транзакции которую необходимо выполнить.
        :return: True если транзакция выполнена.
        """
        if OrganizationTransaction.objects.filter(id=transaction_id).exists():
            transaction = OrganizationTransaction.objects.select_for_update(
                of=('self',),
            ).filter(id=transaction_id).first()
            balance_obj = Organization.objects.select_for_update(
                of=('self',),
            ).filter(id=transaction.organization_id).first()
        elif InspectorTransaction.objects.filter(id=transaction_id).exists():
            transaction = InspectorTransaction.objects.select_for_update(
                of=('self',),
            ).filter(id=transaction_id).first()
            balance_obj = Inspector.objects.select_for_update(
                of=('self',),
            ).filter(id=transaction.inspector_id).first()
        else:
            return False

        transaction_result = False
        if transaction.type == TransactionTypes.WITHDRAW:
            transaction_result = self._withdraw(transaction, balance_obj)
        elif transaction.type == TransactionTypes.ADD:
            transaction_result = self._add(transaction, balance_obj)

        if not transaction_result:
            transaction.status = TransactionStatuses.ERROR

        balance_obj.save()
        transaction.save()
        return transaction_result

    def _add(self, transaction: Union[OrganizationTransaction, InspectorTransaction], balance_obj) -> bool:
        """Начисление.

        :param transaction: транзакция.
        """
        balance_obj.balance = F('balance') + transaction.amount
        transaction.status = TransactionStatuses.DONE
        return True

    def _withdraw(self, transaction: Union[OrganizationTransaction, InspectorTransaction], balance_obj) -> bool:
        """Списание.

        :param transaction: транзакция.
        :return: False если у юзера недостатоно баллов.
        """
        if balance_obj.balance < transaction.amount:
            return False
        balance_obj.balance = F('balance') - transaction.amount
        transaction.status = TransactionStatuses.DONE
        return True
