from apps.helpers.services import AbstractService


class ZoneOrderingAsIntService(AbstractService):
    """Сервис сортирует строковые поля как интовые, для корректной сортировки 1-2-3-11-12-13-21-22-23"""

    def process(self, qs, qp):
        if 'ordering' in qp and qp['ordering'] in ('code', '-code'):  # noqa: WPS510
            qs = qs.extra(select={'intcode': "CAST(substring(code FROM '^[0-9]+') AS INTEGER)"})
            if qp['ordering'] == 'code':
                qs = qs.order_by('intcode')
            elif qp['ordering'] == '-code':
                qs = qs.order_by('-intcode')
        return qs
