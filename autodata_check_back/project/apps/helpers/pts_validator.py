from django.core.validators import RegexValidator


class PtsSerialValidator(RegexValidator):
    regex = r'^\d{4,4}$'
    message = 'Серия ПСТ допускает четыре цифры.'


class PtsNumberValidator(RegexValidator):
    regex = r'^\d{6,6}$'
    message = 'Номер ПСТ допускает 6 цифр.'


class PtsDigitalNumberValidator(RegexValidator):
    regex = r'^\d{15,15}$'
    message = 'Номер ПСТ допускает 15 цифр.'
