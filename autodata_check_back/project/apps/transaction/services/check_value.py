from hashlib import md5

from django.conf import settings

from apps.helpers.services import AbstractService
from apps.transaction.models import Transaction


class CheckValueService(AbstractService):  # noqa: WPS338
    """Сервис генерации контрольного кода по формуле из АПК Assist."""

    def __init__(self, transaction: Transaction, order_state=None):  # noqa: D107
        self.transaction = transaction
        self.order_state = order_state

    def _md5_salt(self):
        return md5(settings.ASSIST_SALT.encode()).hexdigest()  # noqa: S303

    def _md5_checksum(self):
        checksum = f'{settings.ASSIST_MERCHANT_ID};{self.transaction.id};{self.transaction.amount};RUB'.encode()
        if self.order_state:
            checksum = f'{settings.ASSIST_MERCHANT_ID}{self.transaction.id}' \
                       f'{self.transaction.amount}RUB{self.order_state}'.encode()  # noqa: WPS326, WPS318
        return md5(checksum).hexdigest()  # noqa: S303

    def process(self):
        md5_salt = self._md5_salt()
        md5_checksum = self._md5_checksum()
        return md5((md5_salt + md5_checksum).upper().encode()).hexdigest().upper()  # noqa: S303
