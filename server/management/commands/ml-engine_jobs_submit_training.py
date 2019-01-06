import logging
import os
import subprocess
import sys
from datetime import datetime

import pytz
from django.conf import settings
from django.core.management import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Submit a training job to ml-engine'

    def add_arguments(self, parser):
        default_bucket_name = os.environ.get('GCLOUD_BUCKET')
        parser.add_argument('--bucket-name', default=default_bucket_name, help='')

        timestamp = datetime.now().strftime('%Y%m%dT%H%M%S')
        prefix = 'netkeiba_'
        default_job_name = ''.join([prefix, timestamp])
        parser.add_argument('--job-name', default=default_job_name, help='')

        default_job_dir = f'gs://{default_bucket_name}/ml-engine/jobs/'
        parser.add_argument('--job-dir', default=default_job_dir, help='')

        default_package_path = os.path.join(settings.BASE_DIR, 'trainer')
        parser.add_argument('--package-path', default=default_package_path, help='')

        parser.add_argument('--module-name', default='trainer.task', help='')
        parser.add_argument('--region', default='us-central1', help='')
        parser.add_argument('--runtime-version', default='1.12', help='')
        parser.add_argument('--python-version', default='3.5', help='')
        parser.add_argument('--scale-tier', default='BASIC', help='')

    def handle(self, *args, **options):
        start_dt = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        logger.info(f'Started submit command at {start_dt}')

        subprocess.check_call([
            'gcloud', 'ml-engine', 'jobs', 'submit', 'training', options['job_name'],
            '--job-dir', options['job_dir'],
            '--package-path', options['package_path'],
            '--module-name', options['module_name'],
            '--region', options['region'],
            '--runtime-version', options['runtime_version'],
            '--python-version', options['python_version'],
            '--scale-tier', options['scale_tier'],
            '--',
            '--bucket-name', options['bucket_name']
        ], stderr=sys.stdout)

        finish_dt = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        duration = (finish_dt - start_dt).seconds
        logger.info(f'Finished submit command at {finish_dt} ({duration} seconds)')
