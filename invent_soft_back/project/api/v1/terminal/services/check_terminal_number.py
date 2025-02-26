from django.db.models import Q
from rest_framework.exceptions import ValidationError

from apps.helpers.services import AbstractService
from apps.terminal.models import Terminal


class CheckTerminalNumberService(AbstractService):
    """Сервис проверяет, что в проекте нет терминала с таким номером."""

    def __init__(self, number: int, device_model, created: bool):
        self.terminal_number = number
        self.device_model = device_model
        self.created = created

    def process(self):  # noqa: WPS238 WPS231
        busy_numbers = []
        if self.created:
            suitable_numbers = list(range(99900, 100000))
        else:
            if self.device_model == 'MC2200':
                suitable_numbers = list(range(3000, 4000))
                if self.terminal_number not in range(3000, 4000):
                    raise ValidationError('Диапазон номеров должен быть от 3000 до 3999')
            if self.device_model == 'NLS-N7':
                suitable_numbers = list(range(4000, 5000))
                if self.terminal_number not in range(4000, 5000):
                    raise ValidationError('Диапазон номеров должен быть от 4000 до 4999')
            if self.device_model != 'MC2200' and self.device_model != 'NLS-N7':  # noqa: WPS514
                raise ValidationError('Неизвестный терминал')
        for terminal in Terminal.objects.filter(Q(number__gte=suitable_numbers[0], number__lte=suitable_numbers[-1])):
            number = terminal.number
            busy_numbers.append(number)
            if number in suitable_numbers:
                suitable_numbers.remove(number)
        if self.terminal_number in busy_numbers:
            raise ValidationError({
                'message': f'Такой номер терминала уже существует. Доступный номер {suitable_numbers[0]}',
                'available_number': suitable_numbers[0],
            })
        return True
