from apps.template.models import Template


def deactivate_templates_signal(sender, instance=None, created=False, **kwargs):
    if instance.is_active:
        Template.objects.filter(user=instance.user, user__is_superuser=False, is_active=True).exclude(
            id=instance.id  # noqa: C812
        ).update(is_active=False)
