from apps import app
from apps.news.services import UpdateIsPublishedNewsMailingService


@app.task
def update_is_published_news_mailing():
    """Публикации новостных рассылок."""
    UpdateIsPublishedNewsMailingService().process()
