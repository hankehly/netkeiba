# Generated by Django 2.1.4 on 2018-12-22 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0011_track_condition_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='race',
            name='url',
        ),
    ]