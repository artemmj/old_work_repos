from django.contrib.auth import get_user_model
from django_filters import FilterSet

User = get_user_model()


class UserFilterSet(FilterSet):
    pass  # noqa: WPS420 WPS604
