from apps import app
from apps.survey.services import UpdateIsPublishedSurveysMailingService


@app.task
def update_is_published_surveys_mailing():
    """Таска публикации опросов."""
    UpdateIsPublishedSurveysMailingService().process()
