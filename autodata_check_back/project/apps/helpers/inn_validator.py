from constance import config
from django.core.exceptions import ValidationError


def inn_control_sum(nums, type):  # noqa: WPS125
    """Подсчет контрольной суммы."""
    inn_ctrl_type = {
        'n2_12': [7, 2, 4, 10, 3, 5, 9, 4, 6, 8],
        'n1_12': [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8],
        'n1_10': [2, 4, 10, 3, 5, 9, 4, 6, 8],
    }

    l = inn_ctrl_type[type]  # noqa: E741
    n = sum(nums[i] * l[i] for i in range(0, len(l)))  # noqa: WPS221
    return n % 11 % 10   # noqa: WPS432


def check_inn(inn):
    """Проверка ИНН на корректность."""
    str_inn = str(inn)
    nums = [int(x) for x in str_inn]
    if len(str_inn) == 10:
        n1 = inn_control_sum(nums, 'n1_10')
        if n1 == nums[-1]:
            return True
    elif len(str_inn) == 12:  # noqa: WPS432
        n2 = inn_control_sum(nums, 'n2_12')
        n1 = inn_control_sum(nums, 'n1_12')
        if n2 == nums[-2] and n1 == nums[-1]:
            return True
    else:
        return False


def inn_validator(data):  # noqa: D103, WPS110
    if data.__contains__('inn'):  # noqa: WPS609
        if not check_inn(data['inn']):
            raise ValidationError(config.INN_INVALID_ERROR)
    else:
        if not check_inn(data):  # noqa: WPS513
            raise ValidationError(config.INN_INVALID_ERROR)
