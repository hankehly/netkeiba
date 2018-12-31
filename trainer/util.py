import gzip
import json
import os
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime

import pandas as pd
from sklearn.externals import joblib

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, 'db.sqlite3')


def read_netkeiba():
    if not os.path.exists(DB_PATH):
        download_latest_db()

    conn = sqlite3.connect(os.path.join(PROJECT_ROOT, 'db.sqlite3'))
    cur = conn.cursor()

    with open(os.path.join(PROJECT_ROOT, 'trainer', 'select_all.sql'), 'r') as f:
        rows = cur.execute(f.read()).fetchall()

        # Get the column names of the last query. To remain compatible with the Python DB API,
        # it returns a 7-tuple for each column where the last six items of each tuple are None.
        cols = [desc[0] for desc in cur.description]

        df = pd.DataFrame(rows, columns=cols)

        df['r_contender_count'] = df.groupby('r_id').c_id.count().loc[df.r_id].values
        df['c_meters_per_second'] = (df['c_finish_time'] / df['r_distance']).round(6)

        label_value_counts = df['c_meters_per_second'].value_counts()
        stray_label_values = label_value_counts.index[label_value_counts < 2].values
        stray_label_bool_mask = df['c_meters_per_second'].isin(stray_label_values)
        stray_label_indices = df[stray_label_bool_mask].index
        df.drop(stray_label_indices, inplace=True)

        # df['is_day'] = None
        # df['h_old_place'] = None

        index_attrs = ['c_id', 'r_id', 'h_id', 'j_id', 't_id', 'r_key', 'h_key', 'j_key', 't_key']
        label_attrs = ['c_order_of_finish', 'c_finish_time', 'c_order_of_finish_lowered', 'c_meters_per_second']

        X = df.drop(columns=index_attrs + label_attrs)
        y = df['c_meters_per_second']

        return X, y


def download_latest_db():
    bucket_name = _get_bucket_name()
    gcs_backup_dir = os.path.join('gs://', bucket_name, 'data', 'db_backups')
    backups = subprocess.check_output(['gsutil', 'ls', gcs_backup_dir], stderr=sys.stdout).splitlines()
    backup_dirname = backups[-1].decode()
    gcs_model_path = os.path.join('gs://', backup_dirname, 'db.sqlite3.gz')
    db_gzip_path = ''.join([DB_PATH, '.gz'])
    subprocess.check_call(['gsutil', 'cp', gcs_model_path, db_gzip_path], stderr=sys.stdout)

    with gzip.open(db_gzip_path, 'rb') as f_in:
        with open(DB_PATH, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def upload_model(model):
    model_filename = 'model.joblib'
    joblib.dump(model, os.path.join(model_filename))
    timestamp = datetime.now().isoformat(timespec='minutes').replace(':', '')
    bucket_name = _get_bucket_name()
    gcs_model_path = os.path.join('gs://', bucket_name, 'ml-engine', 'models', timestamp, model_filename)
    subprocess.check_call(['gsutil', 'cp', model_filename, gcs_model_path], stderr=sys.stdout)


def _get_bucket_name():
    env_bucket_name = os.environ.get('GCLOUD_BUCKET')

    if not env_bucket_name:
        tf_config = os.environ.get('TF_CONFIG', {})

        if not tf_config:
            raise ValueError('unable to infer bucket name: {}'.format(os.environ))

        tf_config_json = json.loads(tf_config)
        job_args = tf_config_json.get('job', {}).get('args')

        if '--bucket-name' in job_args:
            bucket_name_pos = job_args.index('--bucket-name') + 1
            return job_args[bucket_name_pos]

    return env_bucket_name
