"""Константы используемые в моделях django для большинства случаев.

Если вы не знаете какой максимальной длины строка может храниться в
models.CharField используйте тип поля models.TextField.
Оба типа на уровне бд работают с одинаковой производительностью.
Но models.CharField требует чуть больше ресурсов для обработки и
места для хранения из-за ограничения длины.
see: https://www.postgresql.org/docs/12/datatype-character.html
"""

from decimal import Decimal
from typing import Final

CHAR_FIELD_SMALL_LENGTH: Final = 40  # минимальная длина CharField используемая в моделях
CHAR_FIELD_MIDDLE_LENGTH: Final = 150  # минимальная длина CharField используемая в моделях
CHAR_FIELD_MAX_LENGTH: Final = 400  # максимальная длина CharField используемая в моделях

DECIMAL_FIELD_SMALL_LENGTH: Final = 10  # минимальная длина DecimalField используемая в моделях
DECIMAL_FIELD_MAX_LENGTH: Final = 19  # максимальная длина DecimalField используемая в моделях
DECIMAL_FIELD_PLACES_DEFAULT: Final = 2  # кол-во знаков после запятой в DecimalField используемое в моделях

DECIMAL_ZERO_VALUE: Final = Decimal(0)  # 0 типа decimal
FLOAT_ZERO_VALUE: Final = float(0)  # 0 типа float

# etc
CHAR_FIELD_INN_LENGTH: Final = 12

# алиасы для обратной совместимости
CHAR_FIELD_LENGTH_40 = CHAR_FIELD_SMALL_LENGTH
CHAR_FIELD_LENGTH_150 = CHAR_FIELD_MIDDLE_LENGTH
CHAR_FIELD_LENGTH_400 = CHAR_FIELD_MAX_LENGTH

DECIMAL_FIELD_LENGTH_10 = DECIMAL_FIELD_SMALL_LENGTH
DECIMAL_FIELD_LENGTH_19 = DECIMAL_FIELD_MAX_LENGTH
DECIMAL_PLACES_LENGTH_2 = DECIMAL_FIELD_PLACES_DEFAULT

# srid для Point
SRID = 4326
