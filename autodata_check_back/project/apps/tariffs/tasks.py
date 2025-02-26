from django.utils import timezone

from apps import app
from apps.organization.models import Membership, MembershipRoleChoices
from apps.tariffs.models import Subscription
from apps.tariffs.services.activate import ActivateSubscriptionService
from apps.tariffs.services.deactivate import DeactivateSubscriptionService


@app.task
def deactivate_subscriptions():
    """Таска по деактивации активных подписок у которых закончилось время действия."""
    subscription_ids = Subscription.objects.filter(
        is_active=True, end_datetime__lte=timezone.now(),
    ).values_list('id', flat=True)
    DeactivateSubscriptionService().process(subscription_ids)


@app.task
def renewal_subscriptions():
    """Таска по возобновлению деактивированных подпискок."""
    subscriptions = Subscription.objects.filter(is_active=False, auto_renewal=True)
    for sub in subscriptions:
        membership = Membership.objects.filter(
            organization=sub.organization, role=MembershipRoleChoices.OWNER,
        ).first()
        if membership:
            user = membership.user
            ActivateSubscriptionService(sub.tariff, sub.organization, user, subscription=sub).process()
