import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

BOT_NAME = 'netkeiba'

SPIDER_MODULES = ['netkeiba.spiders']
NEWSPIDER_MODULE = 'netkeiba.spiders'

ROBOTSTXT_OBEY = True

COOKIES_ENABLED = False

REDIRECT_ENABLED = False

DUPEFILTER_DEBUG = True

AUTOTHROTTLE_ENABLED = True

DOWNLOAD_DELAY = 1.0

DOWNLOADER_MIDDLEWARES = {
    'netkeiba.middlewares.UserAgentMiddleware': 300,
}
