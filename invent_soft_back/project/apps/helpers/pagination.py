from datetime import datetime
from collections import OrderedDict

from django.utils.translation import gettext_lazy as _
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PerPageNumberPagination(PageNumberPagination):
    page_query_param = 'page'
    page_query_description = _('Страница')
    page_size_query_param = 'per_page'
    page_size_query_description = _('Элементов на странице')
    max_page_size = 50000


class ServerTimePagination(PerPageNumberPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('server_time', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            ('results', data),
        ]))
