import os

from ..common import env

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_CACHE_INDEX = os.environ.get('REDIS_CACHE_INDEX', 3)
REDIS_CACHE_SESSION_INDEX = os.environ.get('REDIS_CACHE_SESSION_INDEX', 4)

CACHES = {
    'default': env.cache(default=f'redis://{REDIS_HOST}/{REDIS_CACHE_INDEX}'),
    'session': env.cache('CACHE_SESSION_URL', default=f'redis://{REDIS_HOST}/{REDIS_CACHE_SESSION_INDEX}'),
}
