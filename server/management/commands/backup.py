import gzip
import logging
import os
import shutil
import sys
from datetime import datetime
from subprocess import PIPE, STDOUT, Popen, check_output

import pytz
from django.conf import settings
from django.core.management import BaseCommand

logger = logging.getLogger(__name__)


def log_proc_output(out):
    with out:
        for line in out:
            logging.info(line)


class Command(BaseCommand):
    help = 'Compress sqlite db and upload to google cloud storage'

    def add_arguments(self, parser):
        parser.add_argument('-k', '--keep-backups', dest='keep_backups', type=int, default=3,
                            help='Number of backups to keep (old backups are deleted)')

    def handle(self, *args, **options):
        start_dt = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        logger.info(f'Started backup command at {start_dt}')

        bucket_name = os.environ.get('GCLOUD_BUCKET')
        ts_fmt = '%Y-%m-%dT%H%M%S'
        timestamp = datetime.now().strftime(ts_fmt)
        gcs_netkeiba_data_dir = os.path.join('gs://', bucket_name, 'data', 'db_backups')
        gcs_backup_path = os.path.join(gcs_netkeiba_data_dir, timestamp, 'db.sqlite3.gz')

        db_path = settings.DATABASES['default']['NAME']
        db_gzip_path = f'{db_path}.gz'

        with open(db_path, 'rb') as f_in:
            with gzip.open(db_gzip_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        cp_proc = Popen(['gsutil', 'cp', db_gzip_path, gcs_backup_path], stderr=STDOUT, stdout=PIPE)
        log_proc_output(cp_proc.stdout)

        backups = check_output(['gsutil', 'ls', gcs_netkeiba_data_dir], stderr=sys.stdout).splitlines()
        keep_backups = options.get('keep_backups')
        for backup in backups[:-keep_backups]:
            backup_path = backup.decode()
            rm_proc = Popen(['gsutil', 'rm', '-r', backup_path], stderr=STDOUT, stdout=PIPE)
            log_proc_output(rm_proc.stdout)

        finish_dt = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        duration = (finish_dt - start_dt).seconds
        logger.info(f'Finished backup command at {finish_dt} ({duration} seconds)')
