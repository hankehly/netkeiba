import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TMP_DIR = os.path.join(BASE_DIR, 'tmp')
LOG_DIR = os.getenv('LOG_DIR', os.path.join(BASE_DIR, 'log'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# from django.core.management.utils import get_random_secret_key
# get_random_secret_key()
SECRET_KEY = os.getenv('SECRET_KEY')

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

DEBUG = ENVIRONMENT == 'development'

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = ['netkeiba']

MIDDLEWARE = []

ROOT_URLCONF = 'config.urls'

TEMPLATES = []

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'custom': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.getenv('CUSTOM_DB_PATH', ''),
    },
}

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
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
        'dlog': {
            'class': 'logging.FileHandler',
            'filters': ['require_debug_true'],
            'level': 'DEBUG',
            'formatter': 'default',
            'filename': os.path.join(LOG_DIR, 'debug.log'),
        },
        'ilog': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'default',
            'filename': os.path.join(LOG_DIR, 'info.log'),
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

## SCRAPY

BOT_NAME = 'netkeiba'

SPIDER_MODULES = ['netkeiba.spiders']
NEWSPIDER_MODULE = 'netkeiba.spiders'

ROBOTSTXT_OBEY = True

COOKIES_ENABLED = False

CRAWL_BFO = os.getenv('CRAWL_BFO', False) == 1

if CRAWL_BFO:
    DEPTH_PRIORITY = 1
    SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
    SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'

AUTOTHROTTLE_ENABLED = True

CONCURRENT_REQUESTS_PER_DOMAIN = 16

DOWNLOAD_DELAY = 1.0

DOWNLOADER_MIDDLEWARES = {
    'netkeiba.middlewares.UserAgentMiddleware': 300,
}

ITEM_PIPELINES = {
    'netkeiba.pipelines.WebPagePipeline': 300,
}

RETRY_TIMES = 4
