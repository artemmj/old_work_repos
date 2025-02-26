ASGI_APPLICATION = 'apps.routing.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('redis', 6379)],
            'capacity': 1000,  # default 100
            'expiry': 20,  # default 60
        },
    },
}
