import logging
from datetime import datetime

import pytz
from django.core.management import BaseCommand

from netkeiba.settings import TIME_ZONE
from crawler.parsers.race import RaceParser
from server.argtype import date_string
from server.models import WebPage, RaceContender

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
            logger.debug(f'only processing webpages updated on or after {limit}')
            queryset = WebPage.objects.filter(updated_at__gte=limit)
        else:
            logger.debug('processing all webpage records')
            queryset = WebPage.objects.all()

        for page in queryset.order_by('-updated_at').iterator():
            parser = page.get_parser()
            logger.debug(f'parsing {page.url} with {parser.__class__.__name__}')
            parser.parse()

            if isinstance(parser, RaceParser):
                pre_save_contender_count = RaceContender.objects.count()
                parsed_contender_count = len(parser.data.get('contenders'))
                parser.persist()
                post_save_contender_count = RaceContender.objects.count()
                logger.debug(f'parsed {parsed_contender_count} contenders (total: {pre_save_contender_count} -> {post_save_contender_count})')
            else:
                parser.persist()

        end_time = datetime.now(pytz.timezone(TIME_ZONE))
        duration = (end_time - start_time).seconds
        logger.info(f'Finished import command at {end_time} ({duration} seconds)')
