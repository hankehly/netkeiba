import logging
from datetime import datetime, timedelta

import pytz
from django.core.management import BaseCommand

from netkeiba.settings import TIME_ZONE
from server.models import WebPage

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Extract, clean and persist scraped HTML stored in WebPage model. By default, only HTML updated in the ' \
           'past 7 days is processed. '

    def add_arguments(self, parser):
        parser.add_argument('-a', '--all', dest='all', action='store_true',
                            help='Process all scraped HTML currently stored in WebPage table')

    def handle(self, *args, **options):
        if options['all']:
            queryset = WebPage.objects.all()
        else:
            one_week_ago = datetime.now(tz=pytz.timezone(TIME_ZONE)) - timedelta(weeks=1)
            queryset = WebPage.objects.filter(updated_at__gte=one_week_ago)

        for page in queryset.order_by('-updated_at').iterator():
            print(f'Processing {page.url}')
            parser = page.get_parser()
            parser.parse()
            parser.persist()
