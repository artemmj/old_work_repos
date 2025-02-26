from django_filters import BooleanFilter, FilterSet

from apps.stories.models import Stories


class StoriesFilterSet(FilterSet):
    read_stories = BooleanFilter(field_name='read_stories')

    class Meta:
        model = Stories
        fields = ()
