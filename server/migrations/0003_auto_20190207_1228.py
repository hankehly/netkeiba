# Generated by Django 2.1.5 on 2019-02-07 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_auto_20190207_0052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='race',
            name='grade',
        ),
        migrations.AlterField(
            model_name='race',
            name='race_class',
            field=models.CharField(choices=[('G1', 'G1'), ('G2', 'G2'), ('G3', 'G3'), ('OPEN', 'Open'), ('U1600', 'Under 1600'), ('U1000', 'Under 1000'), ('U500', 'Under 500'), ('MAIDEN', 'Maiden'), ('UNRACED_MAIDEN', 'Unraced Maiden'), ('UNKNOWN', 'Unknown')], default='UNKNOWN', max_length=255),
        ),
    ]