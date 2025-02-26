import os

from ..common import env

BROKER_URL = os.environ.get('BROKER_URL', 'redis://redis/14')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis/15')
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = env('TIME_ZONE', str, 'Europe/Moscow')
CELERYBEAT_SCHEDULE = {
    'update_is_published_news_mailing_task': {
        'task': 'apps.news.tasks.update_is_published_news_mailing',
        'schedule': 60,
    },
    'update_is_published_promotions_mailing_task': {
        'task': 'apps.promotion.tasks.update_is_published_promotions_mailing',
        'schedule': 60,
    },
    'update_is_published_stories_mailing_task': {
        'task': 'apps.stories.tasks.update_is_published_stories_mailing.update_is_published_stories_mailing',
        'schedule': 60,
    },
    'update_is_published_surveys_mailing_task': {
        'task': 'apps.survey.tasks.update_is_published_surveys_mailing.update_is_published_surveys_mailing',
        'schedule': 60,
    },
    'create_user_in_arketa': {
        'task': 'apps.arketa.tasks.create_user_in_arketa',
        'schedule': 300,
    },
}
