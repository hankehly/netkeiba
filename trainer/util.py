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

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
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
        -- race
           r.id                                                          r_id,
           r.key                                                         r_key,
           r.distance                                                    r_distance,
           r.date                                                        r_date,
    
           (SELECT name FROM racetracks WHERE id = r.racetrack_id)       r_racetrack,
           (SELECT name FROM course_types WHERE id = r.course_type_id)   r_course_type,
           (SELECT name FROM weather_categories WHERE id = r.weather_id) r_weather,
    
           (SELECT name FROM dirt_condition_categories WHERE id = r.dirt_condition_id) r_dirt_condition,
           (SELECT name FROM turf_condition_categories WHERE id = r.turf_condition_id) r_turf_condition,
           (SELECT name FROM impost_categories WHERE id = r.impost_category_id)        r_impost_category,
    
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
           LEFT JOIN races r on c.race_id = r.id
           LEFT JOIN horses h on c.horse_id = h.id
           LEFT JOIN jockeys j on c.jockey_id = j.id
           LEFT JOIN trainers t on c.trainer_id = t.id
    ORDER BY c_id;
"""


def read_netkeiba():
    if not os.path.exists(DB_PATH):
        download_latest_db()

    conn = sqlite3.connect(os.path.join(PROJECT_ROOT, 'db.sqlite3'))
    cur = conn.cursor()
    rows = cur.execute(SELECT_ALL).fetchall()

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
    gcs_model_path = os.path.join('gs://', bucket_name, 'ml-engine', 'models', timestamp, model_filename)
    subprocess.check_call(['gsutil', 'cp', model_filename, gcs_model_path], stderr=sys.stdout)

    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, predictions)

    pd.DataFrame([[rmse, mae]], index=[timestamp], columns=['rmse', 'mae']).to_csv('results.csv')
    subprocess.check_call(['gsutil', 'cp', 'results.csv', gcs_model_path], stderr=sys.stdout)

    joblib.dump(X_test, 'X_test.joblib')
    subprocess.check_call(['gsutil', 'cp', 'X_test.joblib', gcs_model_path], stderr=sys.stdout)

    joblib.dump(y_test, 'y_test.joblib')
    subprocess.check_call(['gsutil', 'cp', 'y_test.joblib', gcs_model_path], stderr=sys.stdout)


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
