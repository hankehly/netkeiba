import os
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

BOT_NAME = 'netkeiba'

SPIDER_MODULES = ['netkeiba.spiders']
NEWSPIDER_MODULE = 'netkeiba.spiders'

ROBOTSTXT_OBEY = True

COOKIES_ENABLED = False

ITEM_PIPELINES = {
    'netkeiba.pipelines.RacePipeline': 300,
}

AUTOTHROTTLE_ENABLED = True

DOWNLOAD_DELAY = 4.0

DOWNLOADER_MIDDLEWARES = {
    'netkeiba.middlewares.UserAgentMiddleware': 300,
}

iso_timestamp = datetime.now().isoformat(timespec='seconds')

LOG_FILE = os.path.join(PROJECT_ROOT, 'logs', f'{iso_timestamp}.log')
FEED_URI = os.path.join(PROJECT_ROOT, 'output', f'{iso_timestamp}.jl')
FEED_FORMAT = 'jsonlines'
