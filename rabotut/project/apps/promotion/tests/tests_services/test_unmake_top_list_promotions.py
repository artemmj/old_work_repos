import os

import pytest

from apps.file.models import Image
from apps.promotion.models import Promotion
from apps.promotion.services import UnmakeTopListPromotionService

pytestmark = [pytest.mark.django_db]


def test_unmake_top_list_promotions(user, image, promotion_factory):
    """Тест проверки открепления списка новостей."""
    preview_main = Image.objects.first()
    preview_standart = Image.objects.first()
    promotion_factory(
        count=3,
        name=(name for name in ['1', '2', '3']),
        preview_main=preview_main,
        preview_standart=preview_standart,
        is_top=True,
    )
    promotions_1 = Promotion.objects.get(name='1')
    promotions_2 = Promotion.objects.get(name='2')
    promotions_ids = [promotions_1.id, promotions_2.id]
    UnmakeTopListPromotionService(promotions_ids=promotions_ids).process()
    assert Promotion.objects.filter(is_top=False).count() == 2
    assert Promotion.objects.filter(is_top=True).count() == 1
    os.remove(image)
