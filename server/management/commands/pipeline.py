from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        one_week_ago = (datetime.now(tz=pytz.timezone(settings.TIME_ZONE)) - timedelta(weeks=1)).strftime('%Y-%m-%d')
        call_command('scrape', min_date=one_week_ago)
        call_command('import', min_date=one_week_ago)
        call_command('backup')
        call_command('submit')
