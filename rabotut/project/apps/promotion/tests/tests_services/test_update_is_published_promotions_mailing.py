import os

import pytest

from apps.file.models import Image
from apps.promotion.models import BasePromotionMailing
from apps.promotion.services import UpdateIsPublishedPromotionsMailingService

pytestmark = [pytest.mark.django_db]


def test_update_is_published_promotions_mailing(image, promotion_factory, base_promotion_mailing_factory):
    """Тест проверки публикаций новостных рассылок."""
    preview_main = Image.objects.first()
    preview_standart = Image.objects.first()
    promotions = promotion_factory(
        count=3,
        name=(name for name in ('1', '2', '3')),
        preview_main=preview_main,
        preview_standart=preview_standart,
        is_top=True,
    )
    base_promotion_mailing_factory(
        count=3,
        promotion=(promotion for promotion in promotions),
        publish_datetime='2024-08-28',
        is_published=(is_pub for is_pub in (False, False, True)),
    )
    UpdateIsPublishedPromotionsMailingService().process()
    assert BasePromotionMailing.objects.filter(is_published=False).count() == 0
    assert BasePromotionMailing.objects.filter(is_published=True).count() == 3
    os.remove(image)
