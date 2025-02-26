from django_filters import CharFilter, FilterSet

from apps.transaction.models.organization import OrganizationTransaction


class OrganizationTransactionFilterSet(FilterSet):
    class Meta:
        model = OrganizationTransaction
        fields = ('organization',)
