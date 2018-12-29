import gzip
import logging
import os
import shutil
import subprocess
import sys
from datetime import datetime

from django.conf import settings
from django.core.management import BaseCommand, CommandError

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Compress sqlite db and upload to google cloud storage'

    def add_arguments(self, parser):
        parser.add_argument('-k', '--keep-backups', dest='keep_backups', type=int, default=3,
                            help='Number of backups to keep (old backups are deleted)')

    def handle(self, *args, **options):
        bucket_name = os.environ.get('GCLOUD_BUCKET')
        ts_fmt = '%Y-%m-%dT%H%M%S'
        timestamp = datetime.now().strftime(ts_fmt)
        gcs_netkeiba_data_dir = os.path.join('gs://', bucket_name, 'data', 'netkeiba')
        gcs_backup_path = os.path.join(gcs_netkeiba_data_dir, timestamp, 'db.sqlite3.gz')

        db_path = settings.DATABASES['default']['NAME']
        db_gzip_path = f'{db_path}.gz'

        with open(db_path, 'rb') as f_in:
            with gzip.open(db_gzip_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        subprocess.check_call(['gsutil', 'cp', db_gzip_path, gcs_backup_path], stderr=sys.stdout)

        backups = subprocess.check_output(['gsutil', 'ls', gcs_netkeiba_data_dir], stderr=sys.stdout).splitlines()
        keep_backups = options.get('keep_backups')
        for backup in backups[:-keep_backups]:
            subprocess.check_call(['gsutil', 'rm', '-r', backup.decode()])
