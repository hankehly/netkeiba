# Generated by Django 2.1.4 on 2019-01-14 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0018_auto_20190113_0241'),
    ]

    operations = [
        migrations.AddField(
            model_name='horse',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
