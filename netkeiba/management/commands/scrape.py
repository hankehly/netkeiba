import os
from datetime import datetime

import pytz
from django.core.management import BaseCommand
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from twisted.internet import reactor

from netkeiba import settings
from netkeiba.argtype import date_string
from netkeiba.spiders.db_race import DBRaceSpider


class Command(BaseCommand):
    help = 'Start netkeiba db scrapy spider'

    def add_arguments(self, parser):
        parser.add_argument('--scrape-job-dirname', dest='scrapy_job_dirname',
                            help='Name to use as scrapy job directory. By default, this value is generated at runtime.')
        parser.add_argument('--min-date', dest='min_date', type=date_string,
                            help='Scrape all races that come on or after this date (fmt: YYYY-MM-DD)')
        parser.add_argument('--max-date', dest='max_date', type=date_string,
                            help='Scrape all races that come on or before this date (fmt: YYYY-MM-DD)')

    def handle(self, *args, **options):
        crawls_dir = os.path.join(settings.TMP_DIR, 'crawls')
        if not os.path.isdir(crawls_dir):
            os.makedirs(crawls_dir, exist_ok=True)

        piddir = os.path.join(settings.TMP_DIR, 'pids')
        if not os.path.isdir(piddir):
            os.makedirs(piddir, exist_ok=True)

        timestamp = datetime.now(tz=pytz.timezone(settings.TIME_ZONE)).strftime('%Y-%m-%dT%H%M%S')
        job_dirname = options.get('scrapy_job_dirname') if options.get('scrapy_job_dirname') else timestamp
        jobdir = os.path.join(crawls_dir, job_dirname)
        os.makedirs(jobdir)

        pidfile = os.path.join(piddir, f'{job_dirname}.pid')
        with open(pidfile, 'w') as f:
            f.write(str(os.getpid()) + os.linesep)

        custom_settings = {'JOBDIR': jobdir, }

        scrapy_settings = Settings()
        scrapy_settings.setmodule(settings, priority='project')

        spider = DBRaceSpider(min_date=options.get('min_date'), max_date=options.get('max_date'))
        runner = CrawlerRunner({**scrapy_settings, **custom_settings})
        d = runner.crawl(spider)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
