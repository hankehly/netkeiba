import os
from datetime import datetime

from django.conf import settings
from django.core.management import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from server.argtype import date_string


class Command(BaseCommand):
    help = 'Start scrapy spider'

    def add_arguments(self, parser):
        parser.add_argument('--min-date', dest='min_date', type=date_string,
                            help='Scrape all races that come after this date (fmt: YYYY-MM-DD)')

    def handle(self, *args, **options):
        jobdir = os.path.join(settings.TMP_DIR, 'crawls')

        if not os.path.isdir(jobdir):
            os.mkdir(jobdir)

        iso_timestamp = datetime.now().isoformat(timespec='seconds')
        jobpath = os.path.join(jobdir, iso_timestamp)
        os.mkdir(jobpath)

        # TODO: Where can you specify this?
        # pidfile = os.path.join(settings.TMP_DIR, 'pids', iso_timestamp)

        custom_settings = {
            'JOBDIR': jobpath,
            'LOG_FILE': os.path.join(settings.LOG_DIR, f'{iso_timestamp}.log'),
        }

        process = CrawlerProcess({**get_project_settings(), **custom_settings})
        process.crawl('db', options.get('min_date'))
        process.start()
