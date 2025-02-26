from apps import app
from apps.promotion.services import UpdateIsPublishedPromotionsMailingService


@app.task
def update_is_published_promotions_mailing():
    """Публикация акций."""
    UpdateIsPublishedPromotionsMailingService().process()
