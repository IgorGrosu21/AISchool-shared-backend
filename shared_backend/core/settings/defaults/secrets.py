from ..helpers import get_env, get_env_list

SECRET_KEY = get_env('SECRET_KEY')
DEBUG = get_env('ENVIRONMENT') != 'production'

HOST = get_env('HOST')
SELF_URL = f'http{"" if DEBUG else "s"}://{HOST}'
FRONTEND_BASE_URL = "http://localhost:3000" if DEBUG else "https://aischool.md"
ALLOWED_HOSTS = get_env_list('ALLOWED_HOSTS', ['localhost', '127.0.0.1'] if DEBUG else [])
CORS_ALLOWED_ORIGINS = get_env_list('CORS_ALLOWED_ORIGINS', ['http://localhost:3000', 'http://127.0.0.1:3000'] if DEBUG else [])

SERVICE_ID = get_env('SERVICE_ID')
SERVICE_SECRET = get_env('SERVICE_SECRET')