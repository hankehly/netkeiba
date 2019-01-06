import logging
from datetime import datetime, timedelta
from subprocess import call

import pytz
from django.conf import settings
from django.core.management import BaseCommand, call_command

from server.argtype import date_string

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Execute the netkeiba training pipeline (scrape, import, backup, submit)'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--shutdown', action='store_true', default=False,
                            help='Execute shutdown command after pipeline completion')
        parser.add_argument('-m', '--min-date', dest='min_date', type=date_string,
                            help='Process all data from this date to present (fmt: YYYY-MM-DD)')

    def handle(self, *args, **options):
        start_dt = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        logger.info(f'Started pipeline command at {start_dt}')

        if options['min_date']:
            logger.info(f"user specified minimum date is {options['min_date']}")
            min_date = options['min_date']
        else:
            logger.info('user specified minimum date does not exist (defaulting to now - 1 week)')
            min_date = (start_dt - timedelta(weeks=1)).strftime('%Y-%m-%d')

        scrapy_job_dirname = start_dt.strftime('%Y-%m-%dT%H%M%S')
        logger.debug(f'Scrapy job dirname set to {scrapy_job_dirname}')

        call_command('scrape', scrapy_job_dirname, min_date=min_date)
        call_command('import', scrapy_job_dirname)
        call_command('backup')
        call_command('ml-engine_jobs_submit_training')

        finish_dt = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        duration = (finish_dt - start_dt).seconds
        logger.info(f'Finished pipeline command at {finish_dt} ({duration} seconds)')

        if options['shutdown']:
            logger.info('Received shutdown option. Shutting down now.')
            call('sudo shutdown -h now', shell=True)
