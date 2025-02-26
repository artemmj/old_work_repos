from django.db import models


class IssuingTaskChoices(models.TextChoices):
    LEAST_LOADED_USER = 'least_loaded_user', 'Наименее загруженному пользователю'
    CURRENT_USER = 'current_user', 'Текущему пользователю'


class ProductNameChoices(models.TextChoices):
    BY_PRODUCT_CODE = 'by_product_code', 'По коду товара'
    BY_BARCODE = 'by_barcode', 'По штрих-коду'


class UnknownBarcodeChoices(models.TextChoices):
    ALLOW = 'allow', 'Разрешать'
    DISALLOW = 'disallow', 'Запрещать'


class RecalculationDiscrepancyChoices(models.TextChoices):
    SCAN = 'scan', 'Скан'
    CONTROLLER = 'controller', 'УК'


class CheckDMChoices(models.TextChoices):
    WITHOUT_DM_CHECK = 'without_dm_check', 'Без проверки DM'
    ONLY_DM_CHECK = 'only_dm_check', 'Только наличие DM'
    CONFORMITY_DM = 'conformity_dm', 'Соответствие DM и ШК'
    BINDING_DM = 'binding_dm', 'Привязка DM к ШК'


class CheckAMChoices(models.TextChoices):
    WITHOUT_AM_CHECK = 'without_am_check', 'Без проверки AM'
    ONLY_AM_CHECK = 'only_am_check', 'Только наличие AM'
    CONFORMITY_AM = 'conformity_am', 'Соответствие AM и ШК'
