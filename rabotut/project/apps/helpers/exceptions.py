import logging
from typing import Any, Dict, Generator

from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from drf_standardized_errors.formatter import ExceptionFormatter
from drf_standardized_errors.types import ErrorResponse, ExceptionHandlerContext
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler as base_exception_handler

from apps.helpers.logger import get_request_id

logger = logging.getLogger()


class ErrorResponseSerializer(serializers.Serializer):
    attr = serializers.CharField()
    code = serializers.CharField()
    error = serializers.CharField()
    status_code = serializers.IntegerField()


class CustomExceptionFormatter(ExceptionFormatter):
    def __init__(  # noqa: D107
        self,
        exc: exceptions.APIException,
        context: ExceptionHandlerContext,
        original_exc: Exception,
    ):
        super().__init__(exc, context, original_exc)
        self.status_code = exc.status_code

    def format_error_response(self, error_response: ErrorResponse):
        return (
            {
                'attr': error.attr,
                'code': error.code,
                'error': error.detail,
                'status_code': self.status_code,
            }
            for error in error_response.errors
        )


def dotted_exc(exc_detail, field=None) -> Generator[Dict[str, Any], None, None]:
    """Генератор ошибок с dotted нотацией.

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
    # перехватываем ошибки джанговской валидации
    if isinstance(exc, DjangoValidationError):
        exc = ValidationError(detail=as_serializer_error(exc))

    response = base_exception_handler(exc, context)
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if response is not None:
        errors_data = {
            'status_code': exc.status_code,
            'errors': exc.detail,
            'errors_list': list(dotted_exc(exc.detail)),
            'request_id': get_request_id(),
        }
        response.data = errors_data

    if response:
        logger.info(str(response.data))

    return response
