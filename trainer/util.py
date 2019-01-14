import gzip
import json
import os
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime

import numpy as np
import pandas as pd
from sklearn.externals import joblib
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import StratifiedShuffleSplit

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
from trainer.pipeline import full_pipeline

DB_PATH = os.path.join(PROJECT_ROOT, 'db.sqlite3')

SELECT_ALL = """
    SELECT
        -- race_contender
           c.id                                                          c_id,
           c.weight_carried                                              c_weight_carried,
           c.post_position                                               c_post_position,
           c.order_of_finish                                             c_order_of_finish,
           c.order_of_finish_lowered                                     c_order_of_finish_lowered,
           c.finish_time                                                 c_finish_time,
           c.horse_weight                                                c_horse_weight,
           c.horse_weight_diff                                           c_horse_weight_diff,
           c.popularity                                                  c_popularity,
           c.first_place_odds                                            c_first_place_odds,
           (
                SELECT _c.order_of_finish
                FROM race_contenders _c
                LEFT JOIN races _r ON _c.race_id = _r.id
                WHERE _c.horse_id = c.horse_id AND _r.date < r.date
                ORDER BY _r.date DESC
                LIMIT 1
           ) c_previous_order_of_finish,
        -- race
           r.id                                                                                 r_id,
           r.key                                                                                r_key,
           r.distance                                                                           r_distance,
           r.datetime                                                                           r_datetime,
           (SELECT COUNT(_c.id) FROM race_contenders _c WHERE _c.race_id = r.id)                r_contender_count,
           (SELECT name FROM racetracks WHERE id = r.racetrack_id)                              r_racetrack,
           (SELECT name FROM course_types WHERE id = r.course_type_id)                          r_course_type,
           (SELECT name FROM weather_categories WHERE id = r.weather_id)                        r_weather,
           (SELECT name FROM dirt_condition_categories WHERE id = r.dirt_condition_id)          r_dirt_condition,
           (SELECT name FROM turf_condition_categories WHERE id = r.turf_condition_id)          r_turf_condition,
           (SELECT name FROM impost_categories WHERE id = r.impost_category_id)                 r_impost_category,
    
           (SELECT EXISTS(SELECT id FROM non_winner_regional_horse_races WHERE race_id = r.id)) r_is_non_winner_regional_horse_allowed,
           (SELECT EXISTS(SELECT id FROM winner_regional_horse_races WHERE race_id = r.id))     r_is_winner_regional_horse_allowed,
           (SELECT EXISTS(SELECT id FROM regional_jockey_races WHERE race_id = r.id))           r_is_regional_jockey_allowed,
           (SELECT EXISTS(SELECT id FROM foreign_horse_races WHERE race_id = r.id))             r_is_foreign_horse_allowed,
           (SELECT EXISTS(SELECT id FROM foreign_trainer_horse_races WHERE race_id = r.id))     r_is_foreign_horse_and_trainer_allowed,
           (SELECT EXISTS(SELECT id FROM apprentice_jockey_races WHERE race_id = r.id))         r_is_apprentice_jockey_allowed,
           (SELECT EXISTS(SELECT id FROM female_only_races WHERE race_id = r.id))               r_is_female_only,
        -- horse
           h.id                                                          h_id,
           h.key                                                         h_key,
           h.total_races                                                 h_total_races,
           h.total_wins                                                  h_total_wins,
           (SELECT name FROM horse_sexes WHERE id = h.sex_id)            h_sex,
           h.birthday                                                    h_birthday,
           h.user_rating                                                 h_user_rating,
        -- jockey
           j.id                                                          j_id,
           j.key                                                         j_key,
        -- trainer
           t.id                                                          t_id,
           t.key                                                         t_key
    FROM race_contenders c
           LEFT JOIN races r ON c.race_id = r.id
           LEFT JOIN horses h ON c.horse_id = h.id
           LEFT JOIN jockeys j ON c.jockey_id = j.id
           LEFT JOIN trainers t ON c.trainer_id = t.id
    ORDER BY c_id;
"""


def read_netkeiba():
    if not os.path.exists(DB_PATH):
        print('DB not found locally (missing {db_path}). Downloading most recent backup now.'.format(db_path=DB_PATH))
        download_latest_db()

    conn = sqlite3.connect(os.path.join(PROJECT_ROOT, 'db.sqlite3'))
    c = conn.cursor()
    rows = c.execute(SELECT_ALL).fetchall()
    cols = [desc[0] for desc in c.description]

    df = pd.DataFrame(rows, columns=cols)
    df['c_meters_per_second'] = (df['c_finish_time'] / df['r_distance'])

    X = df.drop(columns=['c_order_of_finish', 'c_finish_time', 'c_order_of_finish_lowered', 'c_meters_per_second'])
    y = df['c_meters_per_second']

    return X, y


def split_train_test(X, y):
    # prevent too many instances from being excluded from dataset during stratisfied shuffling split
    # by rounding y to a value with less decimal places
    y_rounded = y.round(3)

    value_counts = y_rounded.value_counts()
    unique_values = value_counts.index[value_counts < 2].values
    unique_mask = y_rounded.isin(unique_values)
    unique_indices = y_rounded[unique_mask].index

    X.drop(unique_indices, inplace=True)
    y.drop(unique_indices, inplace=True)
    y_rounded.drop(unique_indices, inplace=True)

    print('Dropped {num} instances with unique labels'.format(num=len(unique_indices)))

    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_idx, test_idx in sss.split(X, y_rounded):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    return X_train, X_test, y_train, y_test


def download_latest_db():
    bucket_name = _get_bucket_name()
    gcs_backup_dir = os.path.join('gs://', bucket_name, 'data', 'db_backups')
    backups = subprocess.check_output(['gsutil', 'ls', gcs_backup_dir], stderr=sys.stdout).splitlines()
    gcs_backup_dirname = backups[-1].decode()
    gcs_model_path = os.path.join(gcs_backup_dirname, 'db.sqlite3.gz')
    db_gzip_path = ''.join([DB_PATH, '.gz'])
    subprocess.check_call(['gsutil', 'cp', gcs_model_path, db_gzip_path], stderr=sys.stdout)

    with gzip.open(db_gzip_path, 'rb') as f_in:
        with open(DB_PATH, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def upload_model_with_results(model, X_test, y_test):
    model_filename = 'model.joblib'
    timestamp = datetime.now().strftime('%Y-%m-%dT%H%M%S')
    joblib.dump(model, model_filename)
    bucket_name = _get_bucket_name()
    gcs_model_dir = os.path.join('gs://', bucket_name, 'ml-engine', 'models', timestamp)
    gcs_model_path = os.path.join(gcs_model_dir, model_filename)
    subprocess.check_call(['gsutil', 'cp', model_filename, gcs_model_path], stderr=sys.stdout)

    X_test_prep = full_pipeline.fit_transform(X_test)
    predictions = model.predict(X_test_prep)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, predictions)

    results_filename = 'results.csv'
    pd.DataFrame([[timestamp, rmse, mae]], columns=['timestamp', 'rmse', 'mae']).to_csv(results_filename)
    results_gcs_path = os.path.join(gcs_model_dir, results_filename)
    subprocess.check_call(['gsutil', 'cp', results_filename, results_gcs_path], stderr=sys.stdout)

    X_test_filename = 'X_test.joblib'
    joblib.dump(X_test, X_test_filename)
    X_test_gcs_path = os.path.join(gcs_model_dir, X_test_filename)
    subprocess.check_call(['gsutil', 'cp', X_test_filename, X_test_gcs_path], stderr=sys.stdout)

    y_test_filename = 'y_test.joblib'
    joblib.dump(y_test, y_test_filename)
    y_test_gcs_path = os.path.join(gcs_model_dir, y_test_filename)
    subprocess.check_call(['gsutil', 'cp', y_test_filename, y_test_gcs_path], stderr=sys.stdout)


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
