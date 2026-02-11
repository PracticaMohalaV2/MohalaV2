import os
from pathlib import Path
import dj_database_url

# Rutas base
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY y DEBUG
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-yw8ipn#h#l*3rau(91-_*@hou*2ra=wkota3mriwczp8pupd=i')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Dominios permitidos (Adaptado a Mohala)
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,mohala-production.up.railway.app').split(',')

# Confianza explícita para CSRF
CSRF_TRUSTED_ORIGINS = [
    'https://mohala-production.up.railway.app'
]

# Aplicaciones (Tu app es cuestionario)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cuestionario',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Sistema_Mohala.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'Sistema_Mohala.wsgi.application'

# --- 🗄️ BASE DE DATOS (Lógica de tu proyecto anterior) ---
MYSQL_URL = os.environ.get('MYSQL_URL') or os.environ.get('DATABASE_URL')

if MYSQL_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            MYSQL_URL,
            conn_max_age=600,
            ssl_require=False
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Idioma y hora (Tu ajuste a Santiago)
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] if os.path.exists(os.path.join(BASE_DIR, 'static')) else []

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Seguridad adicional de tu proyecto anterior
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'login'