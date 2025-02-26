from django_filters import BooleanFilter, FilterSet

from apps.survey.models import Survey


class SurveyFilterSet(FilterSet):
    is_published = BooleanFilter(field_name='mailings__is_published')

    class Meta:
        model = Survey
        fields = ('is_self_option',)
