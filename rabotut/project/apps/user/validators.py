from typing import Iterable

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible

INN_ONLY_NUMBERS_ERROR = 'ИНН должен состоять из 12 цифр.'
INN_ERROR = 'Введи правильный номер ИНН.'

check_format = RegexValidator(regex='^[0-9]{12}$', message=INN_ONLY_NUMBERS_ERROR)


@deconstructible
class InnValidator:
    def __call__(self, inn):  # noqa: WPS210
        check_format(inn)
        num11 = int(inn[10])
        num12 = int(inn[11])  # noqa: WPS432
        num11_ok = self.check_low_coefficient(inn, (7, 2, 4, 10, 3, 5, 9, 4, 6, 8)) == num11  # noqa: WPS221
        num12_ok = self.check_low_coefficient(inn, (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8)) == num12  # noqa: WPS221
        is_ok = num11_ok and num12_ok
        if not is_ok:
            raise ValidationError(INN_ERROR)

    @staticmethod
    def check_low_coefficient(inn, coefficients: Iterable[int]) -> int:  # noqa: WPS430
        """
        :param inn: ИНН
        :param coefficients: массив коэффициентов для расчета
        :return: младший разряд суммы произведений разрядов ИНН на маску коэффициентов
        """
        n = 0
        for i, coef in enumerate(coefficients):  # noqa: WPS519
            n += coef * int(inn[i])
        return n % 11 % 10  # noqa: WPS432


INN_VALIDATORS = (InnValidator(),)
