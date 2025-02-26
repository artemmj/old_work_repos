from django.db import models

from apps.helpers.models import CreatedModel, UUIDModel
from apps.inspector.models import Inspector

ACCOUNT_NUMBER_MAX_LEN = 31
BANK_MAX_LEN = 31
BIK_MAX_LEN = 15
INN_MAX_LEN = 15
KPP_MAX_LEN = 15
CORR_ACC_MAX_LEN = 31


class Requisite(UUIDModel, CreatedModel):
    inspector = models.OneToOneField(Inspector, models.CASCADE, related_name='requisite')
    account_number = models.CharField('Номер счета', max_length=ACCOUNT_NUMBER_MAX_LEN)
    bank = models.CharField('Банк получателя', max_length=BANK_MAX_LEN, null=True, blank=True)
    bik = models.CharField('БИК', max_length=BIK_MAX_LEN)
    inn = models.CharField('ИНН', max_length=INN_MAX_LEN)
    kpp = models.CharField('КПП', max_length=KPP_MAX_LEN, null=True, blank=True)
    correspondent_account = models.CharField('Корр.счет', max_length=CORR_ACC_MAX_LEN, null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Реквизиты инспектора'
        verbose_name_plural = 'Реквизиты инспектора'
