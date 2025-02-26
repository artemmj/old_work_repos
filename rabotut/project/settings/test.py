import environ

env = environ.Env(
    DEBUG=(bool, True),
)

DEBUG = env('DEBUG')

if DEBUG:
    from .dev import *  # noqa
else:
    from .production import *  # noqa

# Во время сборки тестов происходит ошибка связанная с использованием django-constance и глобальным импортом через *
# pytest не может получить доступ к бд и запуск тестов падает. По этому внутри тест кейсов мы изменяем backend для
# django-constance c бд на in memory (https://django-constance.readthedocs.io/en/latest/testing.html#memory-backend)
CONSTANCE_BACKEND = 'constance.backends.memory.MemoryBackend'
# отдельный индекс для безболезненной очистки кеша в тестах
CACHES = {
    'default': env.cache(default=f'redis://{REDIS_HOST}/9'),
    'session': env.cache('CACHE_SESSION_URL', default=f'redis://{REDIS_HOST}/{REDIS_CACHE_SESSION_INDEX}'),
}
