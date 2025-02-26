from enum import Enum
from typing import List, Union

import coreschema
import django_filters
from django import forms
from django.db import models
from django.db.models.constants import LOOKUP_SEP
from django.utils.datastructures import MultiValueDict
from django_filters.constants import EMPTY_VALUES
from django_filters.fields import BaseCSVField
from django_filters.filters import Filter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.widgets import BaseCSVWidget
from drf_yasg import openapi
from rest_framework.filters import SearchFilter


class ListFilter(Filter):
    """
    ListFilter позволяет производить фильтрацию по спискам значений, разделённых запятыми.

    Примерное использование: <поле> = ListFilter(field_name='<название в модели>',
    queryset=<модель>.objects.all(), lookup_expr='in')
    """

    def filter(self, queryset, value):    # noqa: WPS221, WPS110
        if value in EMPTY_VALUES:
            return queryset
        return super().filter(queryset, [item.strip() for item in value.split(',')])    # noqa:  WPS110, WPS221


class MultipleParamVersion(str, Enum):    # noqa: WPS600
    COMMA_SEPARATED = '1'    # noqa:  WPS115
    DUPLICATE_PARAMETER = '2'    # noqa:  WPS115


class MultipleParameterWidget(BaseCSVWidget):
    param_name: str = 'param_version'
    default_version: MultipleParamVersion = MultipleParamVersion.COMMA_SEPARATED

    def value_from_datadict(self, data: Union[MultiValueDict, dict], files, name):    # noqa:  WPS110, WPS231
        param_version: str = data.get(self.param_name, self.default_version)

        if not isinstance(data, MultiValueDict):
            if name in data and not isinstance(data[name], List):
                data[name] = [data[name]]
            data = MultiValueDict(data)    # noqa:  WPS110

        values_list: List[str] = []
        if param_version == MultipleParamVersion.COMMA_SEPARATED:
            for item in data.getlist(name):    # noqa:  WPS110
                if not isinstance(item, str):
                    continue
                values_list.extend(x.strip() for x in item.rstrip(',').split(','))   # noqa:  WPS221
        elif param_version == MultipleParamVersion.DUPLICATE_PARAMETER:
            values_list = data.getlist(name)

        if values_list:
            values_list = [{x for x in values_list if x}]

        return values_list


class MultipleParameterField(BaseCSVField):
    widget = MultipleParameterWidget


class CustomBaseInFilter(django_filters.BaseInFilter):
    base_field_class = MultipleParameterField


class IntegerFilter(django_filters.Filter):
    field_class = forms.IntegerField


class IntegerInFilter(CustomBaseInFilter, IntegerFilter):
    pass    # noqa:  WPS420, WPS604


class UUIDInFilter(CustomBaseInFilter, django_filters.UUIDFilter):
    pass    # noqa:  WPS420, WPS604


class CharInFilter(CustomBaseInFilter, django_filters.CharFilter):
    pass    # noqa:  WPS420, WPS604


class ChoiceInFilter(CustomBaseInFilter, django_filters.ChoiceFilter):
    pass   # noqa:  WPS420, WPS604


class SearchFilterWithoutDistinct(SearchFilter):
    """
    Кастомный SearchFilter, который никогда не делает distinct.

    Стандартный фильтр делает distinct в тех случаях, если в названии поля есть __,
    потому что в таком случае, скорее всего, связь у моделей M2M.
    Однако такое поведение некорректно, ведь через __ могут задаваться различные параметры, например name__unaccent.
    В таком случае будет вылетать ошибка.
    """

    def must_call_distinct(self, queryset, search_fields):  # noqa:  WPS231, WPS210
        for search_field in search_fields:
            if search_field.find('unaccent') != -1:
                continue
            opts = queryset.model._meta  # noqa:  WPS437
            if search_field[0] in self.lookup_prefixes:
                search_field = search_field[1:]
            # Annotated fields do not need to be distinct
            if isinstance(queryset, models.QuerySet) and search_field in queryset.query.annotations:
                return False
            parts = search_field.split(LOOKUP_SEP)
            for part in parts:
                field = opts.get_field(part)
                if hasattr(field, 'get_path_info'):  # noqa: WPS421
                    # This field is a relation, update opts to follow the relation
                    path_info = field.get_path_info()
                    opts = path_info[-1].to_opts
                    if any(path.m2m for path in path_info):
                        # This field is a m2m relation so we know we need to call distinct
                        return True  # noqa:  WPS220
        return False


class CustomDjangoFilterBackend(DjangoFilterBackend):
    def get_coreschema_field(self, filter_field: django_filters.Filter):
        """
        Получение schema для фильтров.

        Генерация coreschema для фильтров.
        :param filter_field: поле-фильтр FilterSet.
        """
        # для ModelChoiceFilter надо вычислять queryset, поэтому скип
        if type(filter_field) is django_filters.ModelChoiceFilter:  # noqa:  WPS516
            return super().get_coreschema_field(filter_field)

        if isinstance(filter_field, django_filters.BaseInFilter):
            return coreschema.Array(
                description=str(filter_field.extra.get('help_text', '')),
                items=self.make_single_field(filter_field, main_kwargs=False),
            )
        return self.make_single_field(filter_field)

    def make_single_field(self, filter_field: django_filters.Filter, *, main_kwargs: bool = True):
        kwargs = {}
        if main_kwargs:
            kwargs.update(
                {
                    'description': str(filter_field.extra.get('help_text', '')),
                },
            )

        if isinstance(filter_field, django_filters.DateFilter):
            return coreschema.String(
                **kwargs,
                format=openapi.FORMAT_DATE,
            )
        elif isinstance(filter_field, django_filters.DateTimeFilter):
            return coreschema.String(
                **kwargs,
                format=openapi.FORMAT_DATETIME,
            )
        elif isinstance(filter_field, django_filters.UUIDFilter):
            return coreschema.String(
                **kwargs,
                format=openapi.FORMAT_UUID,
            )
        elif isinstance(filter_field, django_filters.ChoiceFilter):
            return coreschema.Enum(
                **kwargs,
                enum=[
                    choice[0]
                    for choice in filter_field.extra.get('choices', [])
                ],
            )
        return super().get_coreschema_field(filter_field)  # noqa: WPS613
