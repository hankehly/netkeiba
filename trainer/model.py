import logging
import numpy as np
import os
import pandas as pd
import sys
from datetime import datetime

from scipy.stats import randint
from sklearn.ensemble import RandomForestRegressor
from sklearn.externals import joblib
from sklearn.model_selection import RandomizedSearchCV

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

np.random.seed(42)


def train_forest_random_search(X_train_prep, y_train):
    param_distributions = {
        'n_estimators': randint(low=1, high=200),
        'max_features': randint(low=1, high=8),
    }

    forest_reg = RandomForestRegressor(random_state=42)
    rand_search = RandomizedSearchCV(forest_reg, param_distributions=param_distributions, n_iter=25, cv=5,
                                     scoring='neg_mean_squared_error', random_state=42, verbose=5, n_jobs=-1)

    rand_search.fit(X_train_prep, y_train)

    timestamp = datetime.now().isoformat(timespec='minutes').replace(':', '')
    filename = f'forest_reg_{timestamp}.gz'
    joblib.dump(rand_search, filename)

    logging.debug(f'Training complete. Output {filename}')


def predict(X):
    raise NotImplementedError


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

    # upcoming race lists are posted on pages like the following
    # https://race.netkeiba.com/?pid=race_old&id=c201809050103
    # you should be able to take a URL as input and get all the data you need via parsing..
    # because inputting it by hand takes forever.

    # http://db.netkeiba.com/race/201808050703/
    r_racetrack = 'kyoto'
    r_course_type = 'turf'
    r_weather = 'sunny'
    r_distance = 1600
    r_date = '2018-11-24'
    r_dirt_condition = ''
    r_turf_condition = 'good'
    r_impost_category = 'age_based'
    r_is_non_winner_regional_horse_allowed = 1
    r_is_winner_regional_horse_allowed = 0
    r_is_regional_jockey_allowed = 0
    r_is_foreign_horse_allowed = 0
    r_is_foreign_horse_and_trainer_allowed = 0
    r_is_apprentice_jockey_allowed = 0
    r_is_female_only = 0

    # dynamically calculated attrs (but needed from user upon prediction)
    contender_count = 11

    X_test_raw = pd.DataFrame([
        [  # 1st horse
            55,  # c_weight_carried
            6,  # c_post_position
            478,  # c_horse_weight
            -4,  # c_horse_weight_diff
            1,  # c_popularity
            2.7,  # c_first_place_odds
            2,  # h_total_races
            1,  # h_total_wins
            'male',  # h_sex
            '2016-02-10',  # h_birthday
            2.5,  # h_user_rating

            915,  # j_career_1st_place_count
            696,  # j_career_2nd_place_count
            540,  # j_career_3rd_place_count
            2864,  # j_career_4th_place_or_below_count
            2742,  # j_career_turf_race_count
            556,  # j_career_turf_win_count
            2273,  # j_career_dirt_race_count
            359,  # j_career_dirt_win_count
            .182,  # j_career_1st_place_rate
            .321,  # j_career_1st_2nd_place_rate
            .429,  # j_career_any_place_rate
            2146768.,  # j_career_earnings

            409,  # t_career_1st_place_count
            386,  # t_career_2nd_place_count
            406,  # t_career_3rd_place_count
            3635,  # t_career_4th_place_or_below_count
            2795,  # t_career_turf_race_count
            247,  # t_career_turf_win_count
            1958,  # t_career_dirt_race_count
            153,  # t_career_dirt_win_count
            .085,  # t_career_1st_place_rate
            .164,  # t_career_1st_2nd_place_rate
            .248,  # t_career_any_place_rate
            854946.4,  # t_career_earnings
        ]
    ], columns=columns)

    # race details
    # details of each horse/jockey/trainer pair

    predict(X_test_raw)
