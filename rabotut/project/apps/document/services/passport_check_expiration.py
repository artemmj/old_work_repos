from datetime import date
from typing import Union

import pendulum

from apps.helpers.services import AbstractService, ServiceError


class PassportCheckExrationService(AbstractService):
    second_expiration = 243  # 20 лет и 3 месяца
    third_expiration = 543  # 45 лет и 3 месяца

    def process(self, birth_date: Union[date, str], date_issue: date):
        """Валидация актуальности паспорта."""
        if isinstance(birth_date, str):
            birth_date = pendulum.parse(birth_date)

        birth_date_pendulum = pendulum.datetime(birth_date.year, birth_date.month, birth_date.day)
        date_issue_pendulum = pendulum.datetime(date_issue.year, date_issue.month, date_issue.day)

        age_in_months = birth_date_pendulum.diff(pendulum.now()).in_months()

        if age_in_months < self.second_expiration:
            return

        condition_to_third = age_in_months >= self.third_expiration
        age_to_add = self.third_expiration if condition_to_third else self.second_expiration
        correct_date_issue = birth_date_pendulum.add(months=age_to_add - 3)  # без 3 месяцев
        if date_issue_pendulum < correct_date_issue:
            raise ServiceError('Срок действия паспорта истёк. Загрузите актуальный документ')
