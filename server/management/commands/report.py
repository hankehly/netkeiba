import os

import matplotlib.pyplot as plt
import pandas as pd
import sys
from subprocess import check_output

from django.core.management import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Display a graph of results for previous models'

    def handle(self, *args, **options):
        bucket_name = os.environ.get('GCLOUD_BUCKET')
        gcs_results_glob_path = os.path.join('gs://', bucket_name, 'ml-engine', 'models', '*', 'results.csv')

        # [
        #     b',timestamp,rmse,mae', b'0,2019-01-03T200538,0.0007870776797966111,0.0005824914134489689',
        #     b',timestamp,rmse,mae', b'0,2019-01-04T205812,0.0007876000637520677,0.0005832703882289549',
        #     b',timestamp,rmse,mae', b'0,2019-01-05T203605,0.0007872710059437456,0.0005829181830437582',
        #     b',timestamp,rmse,mae', b'0,2019-01-06T203828,0.0007880767038007224,0.0005837651711422726'
        # ]
        result_lines = check_output(['gsutil', 'cat', gcs_results_glob_path], stderr=sys.stdout).splitlines()

        if not result_lines:
            raise CommandError(f'No results found at {gcs_results_glob_path}')

        cols = result_lines[0].decode().split(',')[1:]
        rows = [row.decode().split(',')[1:] for row in result_lines[1::2]]

        #            timestamp                   rmse                    mae
        # 0  2019-01-03T200538  0.0007870776797966111  0.0005824914134489689
        # 1  2019-01-04T205812  0.0007876000637520677  0.0005832703882289549
        # 2  2019-01-05T203605  0.0007872710059437456  0.0005829181830437582
        # 3  2019-01-06T203828  0.0007880767038007224  0.0005837651711422726
        df = pd.DataFrame(rows, columns=cols)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        plt.plot(df.rmse)
        plt.show()
