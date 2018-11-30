import logging
import os
import pandas as pd
import sys
from datetime import datetime

from sklearn.ensemble import RandomForestRegressor
from sklearn.externals import joblib
from sklearn.model_selection import StratifiedShuffleSplit

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
from scripts.utils import read_netkeiba
from trainer.pipeline import full_pipeline

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


def train():
    """
    Model Preparation
    """
    df = read_netkeiba()

    # TODO: allow input to specify contender count
    df['r_contender_count'] = df.groupby('r_id').c_id.count().loc[df.r_id].values
    df['c_norm_order_of_finish'] = 1.0 - (df.c_order_of_finish - 1) / (df.r_contender_count - 1)

    index_attrs = ['c_id', 'r_id', 'h_id', 'j_id', 't_id', 'r_key', 'r_url', 'h_key', 'h_url', 'j_key', 'j_url',
                   't_key',
                   't_url']

    label_attrs = ['c_norm_order_of_finish', 'c_order_of_finish', 'c_finish_time', 'c_order_of_finish_lowered']

    X = df.drop(columns=index_attrs + label_attrs)
    y = df.c_norm_order_of_finish

    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_idx, test_idx in sss.split(X, y):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

    X_train_prep = full_pipeline.fit_transform(X_train)
    train_forest_random_search(X_train_prep, y_train)


def train_forest_random_search(X_train_prep, y_train):
    forest_reg = RandomForestRegressor()
    forest_reg.fit(X_train_prep, y_train)

    timestamp = datetime.now().isoformat().replace(':', '')
    filename = f'forest_reg_{timestamp}.gz'
    joblib.dump(forest_reg, filename)

    logging.debug(f'Training complete. Output {filename}')


def predict(X):
    raise NotImplementedError


if __name__ == '__main__':
    train()


def prediction_test():
    """
    Input feature order:
    """
    columns = [
        'c_id',
        'c_weight_carried',
        'c_post_position',
        'c_order_of_finish',
        'c_order_of_finish_lowered',
        'c_finish_time',
        'c_horse_weight',
        'c_horse_weight_diff',
        'c_popularity',
        'c_first_place_odds',
        'r_id',
        'r_key',
        'r_racetrack',
        'r_course_type',
        'r_weather',
        'r_url',
        'r_distance',
        'r_date',
        'r_dirt_condition',
        'r_turf_condition',
        'r_impost_category',
        'r_is_non_winner_regional_horse_allowed',
        'r_is_winner_regional_horse_allowed',
        'r_is_regional_jockey_allowed',
        'r_is_foreign_horse_allowed',
        'r_is_foreign_horse_and_trainer_allowed',
        'r_is_apprentice_jockey_allowed',
        'r_is_female_only',
        'h_id',
        'h_key',
        'h_url',
        'h_total_races',
        'h_total_wins',
        'h_sex',
        'h_birthday',
        'h_user_rating',
        'j_id',
        'j_key',
        'j_url',
        'j_career_1st_place_count',
        'j_career_2nd_place_count',
        'j_career_3rd_place_count',
        'j_career_4th_place_or_below_count',
        'j_career_turf_race_count',
        'j_career_turf_win_count',
        'j_career_dirt_race_count',
        'j_career_dirt_win_count',
        'j_career_1st_place_rate',
        'j_career_1st_2nd_place_rate',
        'j_career_any_place_rate',
        'j_career_earnings',
        't_id',
        't_key',
        't_url',
        't_career_1st_place_count',
        't_career_2nd_place_count',
        't_career_3rd_place_count',
        't_career_4th_place_or_below_count',
        't_career_turf_race_count',
        't_career_turf_win_count',
        't_career_dirt_race_count',
        't_career_dirt_win_count',
        't_career_1st_place_rate',
        't_career_1st_2nd_place_rate',
        't_career_any_place_rate',
        't_career_earnings',
    ]

    # http://db.netkeiba.com/race/201808050703/
    contender_count = 11

    X_test_raw = pd.DataFrame([
        [  # 1st horse
                      # c_id (SKIP)
            55,       # c_weight_carried
            6,        # c_post_position
                      # c_order_of_finish (SKIP)
                      # c_order_of_finish_lowered (SKIP)
                      # c_finish_time (SKIP)
            478,      # c_horse_weight
            -4,       # c_horse_weight_diff
            1,        # c_popularity
            2.7,      # c_first_place_odds
                      # r_id (SKIP)
                      # r_key (SKIP)
            'kyoto',  # r_racetrack
        ]
    ], columns=columns)

    predict(X_test_raw)
