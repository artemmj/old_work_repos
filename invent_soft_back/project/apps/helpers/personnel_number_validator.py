from django.core.validators import RegexValidator


class PersonnelNumberValidator(RegexValidator):
    regex = r'^\d{6,10}$'
    message = 'Табельный номер должен быть в формате 99999999999. Допускается от 6 до 10 цифр.'
