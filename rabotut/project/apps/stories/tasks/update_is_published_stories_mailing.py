from apps import app
from apps.stories.services import UpdateIsPublishedStoriesMailingService


@app.task
def update_is_published_stories_mailing():
    """Публикации сторис рассылок."""
    UpdateIsPublishedStoriesMailingService().process()
