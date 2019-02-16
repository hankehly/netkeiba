import os

from django.apps import apps
from django.conf import settings

DATABASES = getattr(settings, 'DATABASES')

APP_DIR = apps.get_app_config('netkeiba').path

TMP_DIR = getattr(settings, 'NETKEIBA_TMP_DIR', os.path.join(settings.BASE_DIR, 'tmp'))

TIME_ZONE = getattr(settings, 'NETKEIBA_TIME_ZONE', 'UTC')

BOT_NAME = 'netkeiba'
SPIDER_MODULES = ['netkeiba.spiders']
NEWSPIDER_MODULE = 'netkeiba.spiders'

ROBOTSTXT_OBEY = True

COOKIES_ENABLED = getattr(settings, 'NETKEIBA_COOKIES_ENABLED', False)

CRAWL_BFO = getattr(settings, 'NETKEIBA_CRAWL_BFO', False)

if CRAWL_BFO:
    DEPTH_PRIORITY = 1
    SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
    SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'

AUTOTHROTTLE_ENABLED = True

CONCURRENT_REQUESTS_PER_DOMAIN = getattr(settings, 'NETKEIBA_CONCURRENT_REQUESTS_PER_DOMAIN', 6)

DOWNLOAD_DELAY = getattr(settings, 'NETKEIBA_DOWNLOAD_DELAY', 1.0)

RETRY_TIMES = getattr(settings, 'NETKEIBA_RETRY_TIMES', 4)

DOWNLOADER_MIDDLEWARES = {
    'netkeiba.middlewares.UserAgentMiddleware': 300,
}

ITEM_PIPELINES = {
    'netkeiba.pipelines.WebPagePipeline': 300,
}
