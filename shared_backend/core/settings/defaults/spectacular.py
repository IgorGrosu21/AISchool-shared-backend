from ..helpers import get_env

SPECTACULAR_SETTINGS = {
    'TITLE': get_env('SERVICE_ID').replace('-service', '').title() + ' API',
    'VERSION': '1.1.0',
    'SERVE_INCLUDE_SCHEMA': True,
}