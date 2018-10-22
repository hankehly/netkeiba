BOT_NAME = 'netkeiba'

SPIDER_MODULES = ['netkeiba.spiders']
NEWSPIDER_MODULE = 'netkeiba.spiders'

ROBOTSTXT_OBEY = True

COOKIES_ENABLED = False

ITEM_PIPELINES = {
    'netkeiba.pipelines.RacePipeline': 300,
}

AUTOTHROTTLE_ENABLED = True

DOWNLOAD_DELAY = 5.0

DOWNLOADER_MIDDLEWARES = {
    'netkeiba.middlewares.useragent.UserAgentMiddleware': 300,
}
