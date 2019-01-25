import logging

import dateutil.parser
import pandas as pd
import pytz
from django.conf import settings
from django.core.management import BaseCommand

from server.models import WebPage


class Command(BaseCommand):
    help = 'Import results of db_full spider into django'

    def __init__(self):
        super().__init__()
        self.table = None
        self.logger = logging.getLogger(__name__)

    def add_arguments(self, parser):
        parser.add_argument('csv_path', help='The absolute path to the CSV resource containing exported scrapy items')

    def handle(self, *args, **options):
        csv_path = options['csv_path']
        self.logger.debug(f'Loading csv data from {csv_path}')

        i = 1
        for df in pd.read_csv(csv_path, chunksize=1000):
            self.logger.info(f'processing chunk {i}')
            for j, item in df.iterrows():
                self.logger.debug(f'chunk: {i}, item: {j} <url: {item.url}, fingerprint: {item.fingerprint}>')
                tzinfo = pytz.timezone(settings.TIME_ZONE)
                crawled_at = dateutil.parser.isoparse(item.crawled_at).replace(tzinfo=tzinfo)
                defaults = {'html': item.html, 'url': item.url, 'crawled_at': crawled_at}
                WebPage.objects.update_or_create(fingerprint=item.fingerprint, defaults=defaults)
            i += 1
