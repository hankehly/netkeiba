import os

from django.apps import apps
from django.conf import settings

NAMESPACE = apps.get_app_config('netkeiba').name.upper()

LOG_DIR = getattr(
    settings,
    f'{NAMESPACE}_LOG_DIR',
    os.path.join(settings.BASE_DIR, 'log')
)

TMP_DIR = getattr(
    settings,
    f'{NAMESPACE}_TMP_DIR',
    os.path.join(settings.BASE_DIR, 'tmp')
)

TIME_ZONE = getattr(
    settings,
    f'{NAMESPACE}_TIME_ZONE',
    'UTC'
)

BOT_NAME = NAMESPACE
SPIDER_MODULES = ['netkeiba.spiders']
NEWSPIDER_MODULE = 'netkeiba.spiders'
ROBOTSTXT_OBEY = True

COOKIES_ENABLED = getattr(
    settings,
    f'{NAMESPACE}_COOKIES_ENABLED',
    False
)

CRAWL_BFO = getattr(
    settings,
    f'{NAMESPACE}_CRAWL_BFO',
    False
)

if CRAWL_BFO:
    DEPTH_PRIORITY = 1
    SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
    SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'

AUTOTHROTTLE_ENABLED = True

CONCURRENT_REQUESTS_PER_DOMAIN = getattr(
    settings,
    f'{NAMESPACE}_CONCURRENT_REQUESTS_PER_DOMAIN',
    16
)

DOWNLOAD_DELAY = getattr(
    settings,
    f'{NAMESPACE}_DOWNLOAD_DELAY',
    1.0
)

RETRY_TIMES = getattr(
    settings,
    f'{NAMESPACE}_RETRY_TIMES',
    4
)

DOWNLOADER_MIDDLEWARES = {
    'netkeiba.middlewares.UserAgentMiddleware': 300,
}

ITEM_PIPELINES = {
    'netkeiba.pipelines.WebPagePipeline': 300,
}
