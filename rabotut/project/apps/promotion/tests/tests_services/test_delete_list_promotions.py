import os

import pytest

from apps.file.models import Image
from apps.promotion.models import Promotion
from apps.promotion.services import DeleteListPromotionService

pytestmark = [pytest.mark.django_db]


def test_delete_list_promotions(user, image, promotion_factory):
    """Тест проверки удаления списка акций."""
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
    DeleteListPromotionService(promotions_ids=promotions_ids).process()
    assert Promotion.objects.non_deleted().count() == 1
    os.remove(image)
