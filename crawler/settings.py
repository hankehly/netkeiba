import os
import sys

import django

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

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')

AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')

DYNAMODB_PIPELINE_REGION_NAME = os.getenv('DYNAMODB_PIPELINE_REGION_NAME', '')

DYNAMODB_PIPELINE_TABLE_NAME = os.getenv('DYNAMODB_PIPELINE_TABLE_NAME', '')
