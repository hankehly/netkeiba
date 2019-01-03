import logging
import os
import subprocess
from datetime import datetime

import pytz
from django.conf import settings
from django.core.management import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('dirname', help='The name of the directory containing the model file')

        parser.add_argument('--set-default', action='store_true', default=True, help='Whether to set this version as default model version')  # noqa
        parser.add_argument('--model', default='netkeiba', help='Name of the model (default: netkeiba)')
        parser.add_argument('--description', default='', help='The description of the version (default: "")')
        parser.add_argument('--framework', default='scikit-learn', help='The ML framework used to train this version of the model (default: scikit-learn)')  # noqa
        parser.add_argument('--python-version', default='3.5', help='Version of Python used when creating the version (default: 3.5)')  # noqa
        parser.add_argument('--runtime-version', default='1.12', help='Google Cloud ML Engine runtime version for this job (default: 1.12)')  # noqa
        parser.add_argument('--verbosity', default='warning', help='verbosity levels: debug, info, warning, error, critical, none (default: warning)')  # noqa

    def handle(self, *args, **options):
        start_dt = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        logger.info(f'Started ml-engine_versions_create command at {start_dt}')

        default_bucket_name = os.environ.get('GCLOUD_BUCKET')
        origin = os.path.join('gs://', default_bucket_name, 'ml-engine', 'models', options['dirname'])

        version_prefix = 'v'
        version_title = options['dirname'].replace('-', '')
        version = ''.join([version_prefix, version_title])

        subprocess.check_call([
            'gcloud', 'ml-engine', 'versions', 'create', version,
            '--model', options['model'],
            '--description', options['description'],
            '--framework', options['framework'],
            '--origin', origin,
            '--python-version', options['python_version'],
            '--runtime-version', options['runtime_version'],
            '--verbosity', options['verbosity'],
        ])

        if options['set_default']:
            subprocess.check_call([
                'gcloud', 'ml-engine', 'versions', 'set-default', version,
                '--model', options['model'],
                '--verbosity', options['verbosity'],
            ])

        finish_dt = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        duration = (finish_dt - start_dt).seconds
        logger.info(f'Finished ml-engine_versions_create command at {finish_dt} ({duration} seconds)')
