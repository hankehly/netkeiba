import logging
from datetime import datetime, timedelta

import pytz
from django.core.management import BaseCommand

from netkeiba.settings import TIME_ZONE
from server.argtype import date_string
from server.models import WebPage

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Extract, clean and persist scraped HTML stored in WebPage model. By default, only HTML updated in the ' \
           'past 7 days is processed. '

    def add_arguments(self, parser):
        parser.add_argument('--min-date', dest='min_date', action=date_string,
                            help='Process all scraped HTML from this date to present time (fmt: YYYY-MM-DD)')

    def handle(self, *args, **options):
        if options['min_date']:
            limit = datetime.strptime(options['since'], '%Y-%m-%d')
            queryset = WebPage.objects.filter(updated_at__gte=limit)
        else:
            queryset = WebPage.objects.all()

        for page in queryset.order_by('-updated_at').iterator():
            print(f'Processing {page.url}')
            parser = page.get_parser()
            parser.parse()
            parser.persist()
