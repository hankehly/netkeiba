from datetime import date, timedelta

from django.core.management import call_command


def scrape():
    min_date = (date.today() - timedelta(weeks=1)).strftime('%Y-%m-%d')
    call_command('scrape', min_date=min_date)
