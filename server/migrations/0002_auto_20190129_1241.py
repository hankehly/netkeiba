# Generated by Django 2.1.4 on 2019-01-29 12:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='race',
            options={'get_latest_by': '-datetime'},
        ),
        migrations.AlterField(
            model_name='webpage',
            name='fingerprint',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='webpage',
            name='url',
            field=models.URLField(),
        ),
    ]
