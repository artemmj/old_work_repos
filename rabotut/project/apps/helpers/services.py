from rest_framework import exceptions, settings


class ServiceError(exceptions.APIException):
    status_code = 400
    default_detail = 'Ошибка в работе сервиса'
    default_code = 'service_error'

    def __init__(self, detail=None, code=None):
        detail = {settings.api_settings.NON_FIELD_ERRORS_KEY: detail or self.default_detail}
        super().__init__(detail, code)


class AbstractService:
    """Родитель всех сервисов, все сервисы в системе должны наследоваться от него."""

    def process(self, *args, **kwargs):
        raise NotImplementedError('Should implement this error')
