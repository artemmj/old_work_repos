SWAGGER_SETTINGS = {
    'DOC_EXPANSION': 'none',
    'SECURITY_DEFINITIONS': {
        'Basic': {'type': 'basic'},
        'JWT': {'type': 'apiKey', 'name': 'Authorization', 'in': 'header'},
    },
}
