import structlog
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible

log = structlog.get_logger()

SNILS_ONLY_NUMBERS_ERROR = 'СНИЛС должен состоять из 11 цифр'
SNILS_ERROR = 'Введи правильный номер СНИЛС'

check_format = RegexValidator(regex='^[0-9]{11}$', message=SNILS_ONLY_NUMBERS_ERROR)


@deconstructible
class SNILSValidator:
    def __call__(self, value):  # noqa: WPS231 WPS238 WPS110
        self.check_snils(value)

    @staticmethod
    def check_snils(value: str) -> None:  # noqa: WPS231 WPS238 WPS110
        """Проверка формата и контрольной суммы СНИЛС.

        see https://www.consultant.ru/document/cons_doc_LAW_124607/68ac3b2d1745f9cc7d4332b63c2818ca5d5d20d0/
        """
        check_format(value)
        control_number = value[-2:]
        checksum = sum(int(value[i]) * (9 - i) for i in range(9))  # noqa: WPS221

        if checksum < 100 and str(checksum) != control_number:
            raise ValidationError(SNILS_ERROR)

        if checksum in {100, 101} and control_number != '00':
            raise ValidationError(SNILS_ERROR)

        if checksum == 102 and control_number != '01':  # noqa: WPS432
            raise ValidationError(SNILS_ERROR)

        if str(checksum % 101)[-2:].zfill(2) != control_number:  # noqa: WPS432
            raise ValidationError(SNILS_ERROR)


SNILS_VALIDATORS = (SNILSValidator(),)
