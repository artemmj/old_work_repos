from django.core.validators import RegexValidator

PASSPORT_NUMBER_VALIDATORS = (
    RegexValidator(
        regex='^[0-9]{6}$', message='Номер должен состоять из 6 цифр',
    ),
)

PASSPORT_SERIES_VALIDATORS = (
    RegexValidator(
        regex='^[0-9]{4}$', message='Серия должна состоять из 4 цифр',
    ),
)

PASSPORT_DEPARTMENT_CODE_VALIDATORS = (
    RegexValidator(
        regex='^[0-9]{6}$', message='Код подразделения должен состоять из 6 цифр',
    ),
)
