from django_filters import FilterSet

from apps.document.models import Selfie


class SelfieFilterSet(FilterSet):
    class Meta:
        model = Selfie
        fields = ('user', 'status')
