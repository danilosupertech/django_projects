"""
PT: Configurações principais do projeto Django "setup" do app school-rest.
- Carrega variáveis de ambiente do arquivo `.env` no diretório do projeto.
- Define apps instalados, Django REST Framework, base de dados, idioma e timezone.
- Lê SECRET_KEY/DEBUG/ALLOWED_HOSTS do ambiente e suporta DATABASE_URL (Postgres).

EN: Core Django settings for the "setup" project in school-rest.
- Loads environment variables from the project `.env` file.
- Configures installed apps, Django REST Framework, database, language and timezone.
- Reads SECRET_KEY/DEBUG/ALLOWED_HOSTS from env and supports DATABASE_URL (Postgres).
"""

from pathlib import Path
import os
try:
    from dotenv import load_dotenv  # type: ignore
except Exception:  # PT/EN: Modo degradado quando python-dotenv não está instalado
    def load_dotenv(*_args, **_kwargs):
        return False
from urllib.parse import urlparse


BASE_DIR = Path(__file__).resolve().parent.parent


# PT/EN: Carrega variáveis do arquivo .env na raiz do projeto (se disponível)
load_dotenv(BASE_DIR / '.env')

# PT: Nunca exponha SECRET_KEY em repositórios | EN: Never commit SECRET_KEY
SECRET_KEY = (
    os.getenv('DJANGO_SECRET_KEY')
    or os.getenv('SECRET_KEY')
    or 'dev-insecure-change-me'
)

# PT: DEBUG controlado por env (padrão True em dev) | EN: Default True for dev
DEBUG = os.getenv('DEBUG', 'True').lower() in ('1', 'true', 'yes')

# PT: Hosts permitidos por env (lista separada por vírgula) | EN: Comma-separated
_hosts = os.getenv('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [h.strip() for h in _hosts.split(',') if h.strip()] if _hosts else []
if not ALLOWED_HOSTS and DEBUG:
    ALLOWED_HOSTS = ['*']  # PT: Facilita dev local | EN: Easier local dev


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'escola',
    'rest_framework',
    'rest_framework.authtoken',  # PT/EN: Token auth para APIs
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
        'DIRS': [],
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
    'default': {}
}

# PT: Suporte a DATABASE_URL (ex.: postgres://user:pass@host:5432/dbname)
# EN: Support DATABASE_URL. Fallback to local SQLite.
db_url = os.getenv('DATABASE_URL')
if db_url:
    parsed = urlparse(db_url)
    if parsed.scheme.startswith('postgres'):
        DATABASES['default'] = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': parsed.path.lstrip('/'),
            'USER': parsed.username or '',
            'PASSWORD': parsed.password or '',
            'HOST': parsed.hostname or 'localhost',
            'PORT': str(parsed.port or 5432),
        }
    elif parsed.scheme.startswith('sqlite'):
        DATABASES['default'] = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': parsed.path or (BASE_DIR / 'db.sqlite3'),
        }
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }

REST_FRAMEWORK = {
    # PT: Prefira tokens/sessões a Basic em produção | EN: Prefer token/session over Basic in prod
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    # PT: Leitura anônima; escrita exige permissões de modelo.
    # EN: Anonymous read; writes require Django model permissions.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '60/min',
        'user': '120/min',
    },
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


STATIC_URL = 'static/'  # URL de estáticos | Static files URL

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
