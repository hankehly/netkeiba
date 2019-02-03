from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('url', models.URLField()),
                ('html', models.TextField()),
                ('fingerprint', models.CharField(max_length=255, unique=True)),
                ('crawled_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'webpages',
            },
        ),
    ]
