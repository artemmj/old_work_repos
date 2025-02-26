import os

import pytest

from apps.file.models import Image
from apps.promotion.models import PromotionRead
from apps.promotion.services import GetOrCreatePromotionRead

pytestmark = [pytest.mark.django_db]


def test_create_promotion_read(user, image, promotion_factory):
    """Тест проверки создания прочитанной акции."""
    preview_main = Image.objects.first()
    preview_standart = Image.objects.first()
    promotion = promotion_factory(count=1, preview_main=preview_main, preview_standart=preview_standart)
    GetOrCreatePromotionRead(promotion, user).process()
    assert PromotionRead.objects.count() == 1
    os.remove(image)

def test_get_promotion_read(user, image, promotion_factory, read_promotion_factory):
    """Тест проверки получения прочитанной акции."""
    preview_main = Image.objects.first()
    preview_standart = Image.objects.first()
    promotion = promotion_factory(count=1, preview_main=preview_main, preview_standart=preview_standart)
    read_promotion_factory(count=1, promotion=promotion, user=user)
    GetOrCreatePromotionRead(promotion, user).process()
    assert PromotionRead.objects.count() == 1
    os.remove(image)
