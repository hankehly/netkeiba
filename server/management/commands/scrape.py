import os
from datetime import datetime

from django.conf import settings
from django.core.management import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

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

        piddir = os.path.join(settings.TMP_DIR, 'pids')
        if not os.path.isdir(piddir):
            os.mkdir(piddir)

        iso_timestamp = datetime.now().isoformat(timespec='seconds')
        jobpath = os.path.join(jobdir, iso_timestamp)
        os.mkdir(jobpath)

        pidfile = os.path.join(piddir, f'{iso_timestamp}.pid')
        with open(pidfile, 'w') as f:
            f.write(str(os.getpid()) + os.linesep)

        custom_settings = {
            'JOBDIR': jobpath,
            'LOG_FILE': os.path.join(settings.LOG_DIR, f'{iso_timestamp}.log'),
        }

        scrapy_settings = Settings()
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'crawler.settings'
        settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
        scrapy_settings.setmodule(settings_module_path, priority='project')

        process = CrawlerProcess({**scrapy_settings, **custom_settings})
        process.crawl('db', options.get('min_date'))
        process.start()
