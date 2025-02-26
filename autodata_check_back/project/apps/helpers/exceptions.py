import logging
from typing import Any, Dict, Generator

from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework import exceptions, serializers, status
from rest_framework.views import exception_handler as base_exception_handler

logger = logging.getLogger()


class TokenError(Exception):
    pass  # noqa: WPS604, WPS420


class TokenBackendError(Exception):
    pass  # noqa: WPS604, WPS420


class DetailDictMixin:
    def __init__(self, detail=None, code=None):   # noqa: D107

        detail_dict = {'detail': self.default_detail, 'code': self.default_code}

        if isinstance(detail, dict):
            detail_dict.update(detail)
        elif detail is not None:
            detail_dict['detail'] = detail

        if code is not None:
            detail_dict['code'] = code

        super().__init__(detail_dict)


class CustomAuthenticationFailed(exceptions.AuthenticationFailed):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Не найдено'
    default_code = 'not_found'


class AuthenticationFailed(DetailDictMixin, CustomAuthenticationFailed):
    pass  # noqa: WPS604, WPS420


class BadRequestResponseSerializer(serializers.Serializer):
    status_code = serializers.IntegerField()
    errors = serializers.DictField(child=serializers.ListField())


class ErrorResponseSerializer(serializers.Serializer):
    status_code = serializers.IntegerField()
    errors = serializers.CharField()


def dotted_exc(exc_detail, field=None) -> Generator[Dict[str, Any], None, None]:
    """Генератор ошибок с dotted нотацией.   # noqa: DAR301, D400

    :param exc_detail: ошибка.
    :param field: название текущего поля(необходимо для рекурсии).
    """
    if isinstance(exc_detail, dict):
        for key, error in exc_detail.items():
            field_dotted = f'{field}.{key}' if field else key
            yield from dotted_exc(error, field_dotted)
    else:
        yield {field: exc_detail}


def exception_handler(exc, context):
    """Обработчик ошибок."""
    response = base_exception_handler(exc, context)

    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(detail=serializers.as_serializer_error(exc))
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if getattr(exc, 'detail', None) and not isinstance(exc.detail, dict):
        exc.detail = {'error': exc.detail}

    if getattr(exc, 'detail', None) and exc.detail.get('error') and not isinstance(exc.detail['error'], list):
        error_value = exc.detail['error']
        exc.detail['error'] = [error_value]

    if response is not None:
        errors_data = {
            'status_code': exc.status_code,
            'errors': exc.detail,
            'errors_list': list(dotted_exc(exc.detail)),
        }
        response.data = errors_data

    if response:
        logger.info(str(response.data))

    return response
