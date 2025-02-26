from django_filters import FilterSet

from apps.document.models import Registration


class RegistrationFilterSet(FilterSet):
    class Meta:
        model = Registration
        fields = ('user', 'status')
