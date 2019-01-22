import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TMP_DIR = os.path.join(BASE_DIR, 'tmp')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# django.core.management.utils.get_random_secret_key
SECRET_KEY = os.environ['SECRET_KEY']

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')

AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')

AWS_BUCKET = os.getenv('AWS_BUCKET', '')

DEBUG = ENVIRONMENT == 'development'

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'server'
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

ROOT_URLCONF = 'netkeiba.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'netkeiba.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    )
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

CRONTAB_LOCK_JOBS = True

CRONTAB_COMMAND_PREFIX = f". {os.path.join(BASE_DIR, '.env')};"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'fluentfmt': {
            '()': 'fluent.handler.FluentRecordFormatter',
            'format': {
                'level': '%(levelname)s',
                'hostname': '%(hostname)s',
                'where': '%(module)s.%(funcName)s',
            }
        }
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'level': 'DEBUG',
            'formatter': 'default',
        },
        'fluent': {
            'class': 'fluent.handler.FluentHandler',
            'host': 'localhost',
            'port': 24224,
            'tag': 'netkeiba.default',
            'formatter': 'fluentfmt',
            'level': 'DEBUG',
        },
        'dlog': {
            'class': 'logging.FileHandler',
            'filters': ['require_debug_true'],
            'level': 'DEBUG',
            'formatter': 'default',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
        'ilog': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'default',
            'filename': os.path.join(BASE_DIR, 'info.log'),
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'dlog', 'ilog'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}
