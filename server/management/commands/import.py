import logging
from datetime import datetime

import pytz
from django.core.management import BaseCommand

from netkeiba.settings import TIME_ZONE
from server.argtype import date_string
from server.models import WebPage

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Extract, clean and persist scraped HTML stored in WebPage model'

    def add_arguments(self, parser):
        parser.add_argument('--min-date', dest='min_date', type=date_string,
                            help='Process all scraped HTML from this date to present (fmt: YYYY-MM-DD)')

    def handle(self, *args, **options):
        start_time = datetime.now(pytz.timezone(TIME_ZONE))
        logger.info(f'Started import command at {start_time}')

        if options['min_date']:
            limit = datetime.strptime(options['min_date'], '%Y-%m-%d')
            queryset = WebPage.objects.filter(updated_at__gte=limit)
        else:
            queryset = WebPage.objects.all()

        for page in queryset.order_by('-updated_at').iterator():
            logger.debug(f'Processing {page.url}')
            parser = page.get_parser()
            parser.parse()
            parser.persist()

        end_time = datetime.now(pytz.timezone(TIME_ZONE))
        duration = (end_time - start_time).seconds
        logger.info(f'Finished import command at {end_time} ({duration} seconds)')
