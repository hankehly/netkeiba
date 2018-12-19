from datetime import date, timedelta

from django.core.management import call_command

from server.models import WebPage


def scrape():
    min_date = (date.today() - timedelta(weeks=1)).strftime('%Y-%m-%d')
    call_command('scrape', min_date=min_date)


def import_scraped_content():
    for page in WebPage.objects.all():
        data = page.parse()
        # depending on the type of page
        # it may contain data for one or multiple models
