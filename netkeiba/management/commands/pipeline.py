import logging
from datetime import datetime
from subprocess import call

import pytz
from django.conf import settings
from django.core.management import BaseCommand, call_command

from netkeiba.argtype import date_string

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Execute the netkeiba training pipeline (scrape, import, backup)'

    def add_arguments(self, parser):
        parser.add_argument('--min-date', dest='min_date', type=date_string,
                            help='Scrape all races that come on or after this date (fmt: YYYY-MM-DD)')
        parser.add_argument('--max-date', dest='max_date', type=date_string,
                            help='Scrape all races that come on or before this date (fmt: YYYY-MM-DD)')
        parser.add_argument('--shutdown', action='store_true', default=False,
                            help='Execute shutdown command after pipeline completion')
        parser.add_argument('--backup', action='store_true', default=False,
                            help='Make gzip copy of sqlite database after running scrape and import commands')

    def handle(self, *args, **options):
        started_at = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        logger.info(f'Started pipeline command at {started_at}')

        scrapy_job_dirname = started_at.strftime('%Y-%m-%dT%H%M%S')
        logger.debug(f'Scrapy job dirname set to {scrapy_job_dirname}')

        call_command('scrape', scrapy_job_dirname=scrapy_job_dirname, min_date=options.get('min_date'),
                     max_date=options.get('max_date'))
        call_command('import', scrapy_job_dirname=scrapy_job_dirname)

        if options.get('backup'):
            call_command('backup')

        stopped_at = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        duration = (stopped_at - started_at).seconds
        logger.info(f'Finished pipeline command at {stopped_at} ({duration} seconds)')

        if options.get('shutdown'):
            logger.info('Received shutdown option. Shutting down now.')
            call('sudo shutdown -h now', shell=True)
