"""
PT: Configurações do projeto space-django.
- Carrega variáveis de ambiente de `.env` na raiz (com fallback para `venv/.env`).
- Define apps instalados, templates, base de dados (SQLite), arquivos estáticos e mídia.

EN: Settings for the space-django project.
- Loads env vars from project `.env` (fallback to `venv/.env`).
- Configures installed apps, templates, SQLite DB, static and media files.
"""

from pathlib import Path
try:
    from dotenv import load_dotenv  # type: ignore
except Exception:
    def load_dotenv(*_args, **_kwargs):
        return False
import os

# PT/EN: Carrega .env no diretório do projeto, com fallback para venv/.env
_loaded = load_dotenv(Path(__file__).resolve().parent.parent / '.env')
if not _loaded:
    load_dotenv(Path(__file__).resolve().parent.parent / 'venv' / '.env')

BASE_DIR = Path(__file__).resolve().parent.parent


# PT: Nunca exponha SECRET_KEY em repositórios | EN: Never commit SECRET_KEY
SECRET_KEY = (
    os.getenv('DJANGO_SECRET_KEY')
    or os.getenv('SECRET_KEY')
    or 'dev-insecure-change-me'
)

# PT: DEBUG via env | EN: DEBUG via env
DEBUG = os.getenv('DEBUG', 'True').lower() in ('1', 'true', 'yes')

# PT: Hosts permitidos via env | EN: Allowed hosts via env
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
    'galeria.apps.GaleriaConfig',
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

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Pastas de templates | Template dirs
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'setup.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'pt-pt'

TIME_ZONE = 'Europe/Lisbon'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'  # URL pública de estáticos | Static files URL
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'setup/static'),  # Diretório de estáticos do projeto | Project static dir
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Coleta para produção | Collectstatic target

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Armazenamento de mídia | Media root
MEDIA_URL = '/media/'  # URL pública de mídia | Media URL

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
