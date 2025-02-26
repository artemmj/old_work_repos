from django.db.models import QuerySet, Value
from django.db.models.functions import Coalesce, Length, NullIf, StrIndex, Substr


class DocumentOrderingService:

    def __init__(self, queryset: QuerySet, ordering_param: str):
        self.queryset = queryset
        self.ordering_param = ordering_param

    def process(self) -> QuerySet:
        if self.ordering_param == 'zone_title':
            return self._make_natural_sorting_for(field='zone__title')
        if self.ordering_param == '-zone_title':
            return self._make_natural_sorting_for(field='zone__title', is_reverse=True)

        if self.ordering_param == 'employee_name':
            return self._make_natural_sorting_for(field='employee__username')
        if self.ordering_param == '-employee_name':
            return self._make_natural_sorting_for(field='employee__username', is_reverse=True)

        return self.queryset

    def _make_natural_sorting_for(self, field: str, is_reverse: bool = False) -> QuerySet:
        queryset = self.queryset.order_by(
            Coalesce(
                Substr(
                    field,
                    Value(0),
                    NullIf(
                        StrIndex(field, Value(' ')),
                        Value(0),
                    ),
                ),
                field,
            ),
            Length(field),
            field,
        )

        return queryset.reverse() if is_reverse else queryset
