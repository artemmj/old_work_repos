from apps.organization.models import Membership


def deactivate_membership_signal(sender, instance=None, created=False, **kwargs):
    if instance.is_active:
        Membership.objects.filter(
            user=instance.user,
            is_active=True,
        ).exclude(
            id=instance.id  # noqa: C812
        ).update(is_active=False)
