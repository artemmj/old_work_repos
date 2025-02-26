from django.contrib.auth import get_user_model
from django.db import transaction as db_transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.helpers.services import AbstractService
from apps.organization.models import Organization
from apps.tariffs.models import Subscription, Tariff
from apps.tariffs.services.generate_end_datetime import GenerateEndDatetimeService
from apps.transaction.models import OrganizationTransaction, OrganizationTransactionOperations
from apps.transaction.models.abstract import TransactionStatuses, TransactionTypes

User = get_user_model()


class ActivateSubscriptionService(AbstractService):
    """Сервис активации подписки по тарифу."""

    def __init__(self, tariff: Tariff, organization: Organization, user: User, subscription=None):  # noqa: D107
        self.tariff = tariff
        self.organization = organization
        self.user = user
        self.subscription = subscription

    @db_transaction.atomic()
    def process(self):
        try:  # noqa: WPS229
            transaction = self._create_transaction()
            transaction.refresh_from_db()
            if transaction.status == TransactionStatuses.DONE:
                self._activate_subscription()
        except ValidationError:
            self._deactivate_subscription()

    def _create_transaction(self) -> OrganizationTransaction:
        return OrganizationTransaction.objects.create(
            organization=self.organization,
            user=self.user,
            type=TransactionTypes.WITHDRAW,
            operation=OrganizationTransactionOperations.PAYMENT_TARIFF,
            amount=self.subscription.amount if self.subscription else self.tariff.amount,
        )

    def _activate_subscription(self):
        self.subscription, _ = Subscription.objects.update_or_create(  # noqa: WPS414
            tariff=self.tariff,
            organization=self.organization,
            defaults={
                'amount': self.tariff.amount,
                'is_active': True,
                'auto_renewal': True,
                'start_datetime': timezone.now(),
                'end_datetime': GenerateEndDatetimeService().process(self.tariff),
            },
        )

    def _deactivate_subscription(self):
        if self.subscription:
            self.subscription.is_active = False
            self.subscription.auto_renewal = False
            self.subscription.save()
