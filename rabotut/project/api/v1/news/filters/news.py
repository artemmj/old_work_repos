from django_filters import BooleanFilter, FilterSet

from apps.news.models import News


class NewsFilterSet(FilterSet):
    is_published = BooleanFilter(field_name='news_mailing__is_published')

    class Meta:
        model = News
        fields = ('is_main_page',)
