from django_filters import FilterSet

from apps.document.models import Passport


class PassportFilterSet(FilterSet):
    class Meta:
        model = Passport
        fields = ('user', 'status')
