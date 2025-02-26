from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.utils import timezone

from apps.helpers.services import AbstractService
from apps.tariffs.models import Tariff, TariffPeriodChoices


class GenerateEndDatetimeService(AbstractService):
    """Сервис генерации даты окончания подписки."""

    def process(self, tariff: Tariff) -> datetime:
        period_map = {
            TariffPeriodChoices.WEEK: {'weeks': 1},
            TariffPeriodChoices.MONTH: {'months': 1},
            TariffPeriodChoices.HALF_YEAR: {'months': 6},
            TariffPeriodChoices.YEAR: {'years': 1},
        }
        return timezone.now() + relativedelta(**period_map[tariff.period])
