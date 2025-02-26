import os

from celery.schedules import crontab

from ..common import env

BROKER_URL = os.environ.get('BROKER_URL', 'redis://redis/14')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis/15')
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = env('TIME_ZONE', str, 'Europe/Moscow')
CELERYBEAT_SCHEDULE = {
    'issuing_invitations_task': {
        'task': 'apps.inspection_task.tasks.issuing_invitations',
        'schedule': 30,
    },
    'change_status_expired_tasks_to_draft_task': {
        'task': 'apps.inspection_task.tasks.change_status_expired_tasks_to_draft',
        'schedule': 30,
    },
    'check_balance_replenishment_status_task': {
        'task': 'apps.transaction.tasks.check_balance_replenishment_status.check_balance_replenishment_status',
        'schedule': 30,
    },
    'deactivate_subscriptions_task': {
        'task': 'apps.tariffs.tasks.deactivate_subscriptions',
        'schedule': 30,
    },
    'renewal_subscriptions_task': {
        'task': 'apps.tariffs.tasks.renewal_subscriptions',
        'schedule': 30,
    },
    'cant_get_task_inspector_without_requisite': {
        'task': 'apps.inspection_task.tasks.send_warnings_without_requisite_inspectors',
        'schedule': crontab(minute=0, hour=6),
    },
}
