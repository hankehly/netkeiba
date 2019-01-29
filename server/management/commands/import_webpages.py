import logging
from datetime import datetime

import dateutil.parser
import pandas as pd
import pytz
from django.conf import settings
from django.core.management import BaseCommand
from django.db import IntegrityError

from server.models import WebPage


class Command(BaseCommand):
    help = 'Import results of db_full spider into django'

    def __init__(self):
        super().__init__()
        self.table = None
        self.logger = logging.getLogger(__name__)

    def add_arguments(self, parser):
        parser.add_argument('csv_path', help='The absolute path to the CSV resource containing exported scrapy items')
        parser.add_argument('--chunk-size', type=int, default=1000,
                            help='The chunk size to use when parsing a large CSV file (default 1000)')

    def handle(self, *args, **options):
        tzinfo = pytz.timezone(settings.TIME_ZONE)

        start_time = datetime.now(tzinfo)
        self.logger.info(f'Started import_webpages command at {start_time}')

        csv_path = options['csv_path']
        self.logger.debug(f'Loading csv data from {csv_path}')

        i = 1
        for df in pd.read_csv(csv_path, chunksize=options['chunk_size']):
            self.logger.info(f'processing chunk {i}')
            for j, item in df.iterrows():
                crawled_at = dateutil.parser.isoparse(item.crawled_at).replace(tzinfo=tzinfo)
                defaults = {'fingerprint': item.fingerprint, 'html': item.html, 'url': item.url, 'crawled_at': crawled_at}
                try:
                    WebPage.objects.create(**defaults)
                except IntegrityError:
                    self.logger.debug(f'chunk: {i}, item: {j} already exists <url: {item.url}, fingerprint: {item.fingerprint}>')
                    page = WebPage.objects.get(fingerprint=item.fingerprint)
                    page.url = item.url
                    page.html = item.html
                    page.crawled_at = crawled_at
                    page.save()
                else:
                    self.logger.debug(f'chunk: {i}, item: {j} <url: {item.url}, fingerprint: {item.fingerprint}>')
            i += 1

        end_time = datetime.now(tzinfo)
        duration = (end_time - start_time).seconds
        self.logger.info(f'Finished import_webpages command at {end_time} <{duration}s>')
