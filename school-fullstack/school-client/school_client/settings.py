"""
PT: Configurações do projeto school-client (consome a API school-rest).
- Coloque o arquivo `.env` em `Django/school-fullstack/school-client/.env`.
- `API_BASE_URL` deve apontar para `http://localhost:8001` (não use `0.0.0.0`).

EN: Settings for the school-client project (consumes the school-rest API).
- Put the `.env` file at `Django/school-fullstack/school-client/.env`.
- `API_BASE_URL` should be `http://localhost:8001` (do not use `0.0.0.0`).
"""

from pathlib import Path
import os

try:
    from dotenv import load_dotenv  # type: ignore
except Exception:
    def load_dotenv(*_a, **_k):
        return False

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = (
    os.getenv('DJANGO_SECRET_KEY')
    or os.getenv('SECRET_KEY')
    or 'dev-insecure-change-me'
)

DEBUG = os.getenv('DEBUG', 'True').lower() in ('1', 'true', 'yes')
_hosts = os.getenv('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [h.strip() for h in _hosts.split(',') if h.strip()] if _hosts else []
if not ALLOWED_HOSTS and DEBUG:
    ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'frontend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'school_client.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'school_client.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'pt-pt'
TIME_ZONE = 'Europe/Lisbon'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# PT/EN: Config para consumir a API school-rest
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8001')
API_TOKEN = os.getenv('API_TOKEN', '')
