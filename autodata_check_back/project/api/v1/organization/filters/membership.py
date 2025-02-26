from django.db.models import Q  # noqa: WPS347
from django_filters import BooleanFilter, FilterSet

from apps.organization.models.membership import Membership


class MembershipFilterSet(FilterSet):
    class Meta:
        model = Membership
        fields = ('organization',)
