REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'shared_backend.utils.jwt_authentification.JWTUserAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'shared_backend.utils.renderers.CamelCaseJSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'shared_backend.utils.parsers.CamelCaseJSONParser',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'shared_backend.utils.exception_handler.exception_handler'
}