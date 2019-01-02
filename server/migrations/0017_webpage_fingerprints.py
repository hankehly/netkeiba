# Generated by Django 2.1.4 on 2019-01-02 18:12

from django.db import migrations
from scrapy import Request
from scrapy.utils.request import request_fingerprint


def fill_webpage_fingerprints(apps, schema_editor):
    for page in apps.get_model('server', 'WebPage').objects.filter(fingerprint__exact='').iterator():
        request = Request(page.url)
        page.fingerprint = request_fingerprint(request)
        page.save(update_fields=['fingerprint'])


class Migration(migrations.Migration):
    dependencies = [
        ('server', '0016_webpage_fingerprint'),
    ]

    operations = [
        migrations.RunPython(fill_webpage_fingerprints, migrations.RunPython.noop)
    ]