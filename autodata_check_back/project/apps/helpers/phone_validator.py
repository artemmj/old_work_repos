from django.core.validators import RegexValidator


class PhoneValidator(RegexValidator):
    regex = r'^\+?\d{11,11}$'
    message = 'Телефон должен быть в формате +99999999999 или 99999999999. Допускается от 6 до 15 цифр.'
