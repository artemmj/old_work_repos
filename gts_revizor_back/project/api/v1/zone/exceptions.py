import http

from rest_framework.exceptions import APIException


class ZonesNotEmptyError(APIException):
    status_code = http.HTTPStatus.CONFLICT
    default_detail = 'В переданных зонах есть документы'
    default_code = 'В переданных зонах есть документы'
