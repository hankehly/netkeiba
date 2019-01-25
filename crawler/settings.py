import os
import sys

import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# django integration
sys.path.append(os.path.dirname(os.path.abspath('.')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'netkeiba.settings'
django.setup()

BOT_NAME = 'netkeiba'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

ROBOTSTXT_OBEY = True

COOKIES_ENABLED = False

DUPEFILTER_DEBUG = True

AUTOTHROTTLE_ENABLED = True

DOWNLOAD_DELAY = 1.0

DOWNLOADER_MIDDLEWARES = {
    'crawler.middlewares.UserAgentMiddleware': 300,
}

ITEM_PIPELINES = {
    'crawler.pipelines.DjangoPipeline': 300,
}

RETRY_TIMES = 4
