import os
from datetime import datetime

import pytz
from django.conf import settings
from django.core.management import BaseCommand
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from twisted.internet import reactor

from netkeiba.argtype import date_string


class Command(BaseCommand):
    help = 'Start netkeiba db scrapy spider'

    def add_arguments(self, parser):
        parser.add_argument('--min-date', dest='min_date', type=date_string,
                            help='Scrape all races that come on or after this date (fmt: YYYY-MM-DD)')
        parser.add_argument('--max-date', dest='max_date', type=date_string,
                            help='Scrape all races that come on or before this date (fmt: YYYY-MM-DD)')

    def handle(self, *args, **options):
        crawls_dir = os.path.join(settings.BASE_DIR, 'tmp', 'crawls')
        if not os.path.isdir(crawls_dir):
            os.makedirs(crawls_dir, exist_ok=True)

        piddir = os.path.join(settings.BASE_DIR, 'tmp', 'pids')
        if not os.path.isdir(piddir):
            os.makedirs(piddir, exist_ok=True)

        job_timestamp = datetime.now(tz=pytz.timezone(settings.TIME_ZONE)).strftime('%Y-%m-%dT%H%M%S')
        jobdir = os.path.join(crawls_dir, job_timestamp)
        os.makedirs(jobdir)

        pidfile = os.path.join(piddir, f'{job_timestamp}.pid')
        with open(pidfile, 'w') as f:
            f.write(str(os.getpid()) + os.linesep)

        custom_settings = {'JOBDIR': jobdir}

        scrapy_settings = Settings()
        settings_module_path = os.getenv('SCRAPY_SETTINGS_MODULE')
        scrapy_settings.setmodule(settings_module_path, priority='project')

        runner = CrawlerRunner({**scrapy_settings, **custom_settings})
        d = runner.crawl('db_race', options.get('min_date'), options.get('max_date'))
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
