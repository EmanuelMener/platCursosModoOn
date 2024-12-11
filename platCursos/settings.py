from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-67nrln$_1o@&&&dy8$cyvj)#mek_3o1+-wu^=!_$apw_i0)fwy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['emanuelmene.pythonanywhere.com']





# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'login',
    'cursos',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # Verifique se este middleware está incluído
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.admin_session_middleware.AdminSessionMiddleware',
]


ROOT_URLCONF = 'platCursos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'platCursos.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_REDIRECT_URL = '/cursos/painel/'

# Caso o admin precise ser isolado (opcional):
CSRF_COOKIE_NAME = 'site_csrf'

# Sessões separadas para o admin
SESSION_COOKIE_PATH = '/'
# Identificador de sessão para o admin
ADMIN_SESSION_COOKIE_NAME = "admin_sessionid"
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# Identificador de sessão para o site público
SESSION_COOKIE_NAME = "site_sessionid"
# Nome do cookie para sessões do site principal
SITE_SESSION_COOKIE_NAME = 'site_sessionid'



JAZZMIN_SETTINGS = {
    'site_title': 'Gestor de Cursos',
    'site_name': 'Gestor de Cursos',
    'site_brand': 'Gestor',
    "search_model": ["cursos.Curso", "auth.Group"],
    "show_ui_builder": True,
    "language_chooser": True
}

LANGUAGES = [
    ('en', 'English'),
    ('pt-br', 'Português'),
]



DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY', default='default-secret-key')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Static and Media files
STATIC_ROOT = config('STATIC_ROOT', default=BASE_DIR / 'staticfiles')
MEDIA_ROOT = config('MEDIA_ROOT', default=BASE_DIR / 'mediafiles')


