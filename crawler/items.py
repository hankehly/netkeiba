from datetime import datetime

import pytz
import scrapy
from django.conf import settings
from scrapy.utils.request import request_fingerprint


class BaseWebPageItem(scrapy.Item):
    url = scrapy.Field()
    html = scrapy.Field()
    fingerprint = scrapy.Field()
    crawled_at = scrapy.Field()

    def __repr__(self):
        html = f"{self['html'][:40]}... (truncated)" if len(self['html']) > 55 else self['html']
        return repr({'url': self['url'], 'html': html})

    @classmethod
    def from_response(cls, response):
        fingerprint = request_fingerprint(response.request)
        crawled_at = datetime.now(pytz.timezone(settings.TIME_ZONE)).replace(microsecond=0).isoformat()
        return cls(url=response.url, html=response.text, fingerprint=fingerprint, crawled_at=crawled_at)


# TODO: Rename this class and model to be specific to Netkeiba (ie. NetkeibaWebPageItem)
class WebPageItem(BaseWebPageItem):
    pass


class JMAWebPageItem(BaseWebPageItem):
    pass
