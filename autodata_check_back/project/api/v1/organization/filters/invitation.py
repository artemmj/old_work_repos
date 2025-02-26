from django.db.models import Q  # noqa: WPS347
from django_filters import BooleanFilter, FilterSet

from apps.organization.models import OrgInvitation


class OrgInvitationFilterSet(FilterSet):
    my = BooleanFilter(method='filter_my_invitations')
    is_active = BooleanFilter(method='filter_is_active')

    class Meta:
        model = OrgInvitation
        fields = ('organization',)

    def filter_my_invitations(self, queryset, name, value):  # noqa: WPS110
        if value:
            return queryset.filter(
                Q(user=self.request.user) | Q(phone=self.request.user.phone),
            )
        return queryset

    def filter_is_active(self, queryset, name, value):  # noqa: WPS110
        if value:
            return queryset.filter(is_accepted__isnull=True)
        return queryset
