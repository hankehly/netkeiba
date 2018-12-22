import logging
from datetime import date, timedelta

from django.core.management import call_command

logger = logging.getLogger(__name__)


def scrape():
    one_week_ago = (date.today() - timedelta(weeks=1)).strftime('%Y-%m-%d')
    call_command('scrape', min_date=one_week_ago)


def import_scraped_content():
    one_week_ago = (date.today() - timedelta(weeks=1)).strftime('%Y-%m-%d')
    call_command('import', min_date=one_week_ago)
