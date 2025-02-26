import django_filters

from apps.template.models import TemplateField


class TemplateFieldFilter(django_filters.FilterSet):
    class Meta:
        model = TemplateField
        fields = ('is_reusable',)
