import pytz
from django.db import IntegrityError
from dateutil import parser as date_parser

from . import settings

from netkeiba.models import WebPage


class WebPagePipeline:
    def process_item(self, item, spider):
        tzinfo = pytz.timezone(settings.TIME_ZONE)
        crawled_at = date_parser.isoparse(item['crawled_at']).replace(tzinfo=tzinfo)
        defaults = {'html': item['html'], 'url': item['url'], 'crawled_at': crawled_at}

        try:
            WebPage.objects.create(fingerprint=item['fingerprint'], **defaults)
        except IntegrityError:
            spider.logger.debug(f"update <fingerprint: {item['fingerprint']}, url: {item['url']}>")
            WebPage.objects.filter(fingerprint=item['fingerprint']).update(**defaults)
        else:
            spider.logger.debug(f"insert <fingerprint: {item['fingerprint']}, url: {item['url']}>")

        return item
