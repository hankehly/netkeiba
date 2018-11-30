import pandas as pd

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

cat_attr_categories = {
    'r_racetrack': ['chukyo', 'fuma', 'hakodate', 'hanshin', 'kyoto', 'nakayama', 'niigata', 'ogura', 'sapporo',
                    'tokyo'],
    'r_course_type': ['dirt', 'obstacle', 'turf'],
    'r_weather': ['cloudy', 'rainy', 'snowy', 'sunny'],
    'h_sex': ['castrated', 'female', 'male'],
    'r_impost_category': ['age_based', 'age_sex_based', 'decided_per_race', 'handicap'],
    'r_dirt_condition': ['bad', 'good', 'heavy', 'slightly_heavy'],
    'r_turf_condition': ['bad', 'good', 'heavy', 'slightly_heavy']
}

bool_attrs = [
    'r_is_non_winner_regional_horse_allowed', 'r_is_winner_regional_horse_allowed',
    'r_is_regional_jockey_allowed', 'r_is_foreign_horse_allowed',
    'r_is_foreign_horse_and_trainer_allowed', 'r_is_apprentice_jockey_allowed',
    'r_is_female_only'
]

date_attrs = [
    'r_date', 'h_birthday'
]

num_attrs = [
    'c_weight_carried', 'c_post_position',
    'c_horse_weight', 'c_horse_weight_diff', 'c_popularity',
    'c_first_place_odds', 'r_distance', 'r_contender_count',
    'h_total_races', 'h_total_wins', 'h_user_rating',
    'j_career_1st_place_count', 'j_career_2nd_place_count',
    'j_career_3rd_place_count', 'j_career_4th_place_or_below_count',
    'j_career_turf_race_count', 'j_career_turf_win_count',
    'j_career_dirt_race_count', 'j_career_dirt_win_count',
    'j_career_1st_place_rate', 'j_career_1st_2nd_place_rate',
    'j_career_any_place_rate', 'j_career_earnings',
    't_career_1st_place_count', 't_career_2nd_place_count',
    't_career_3rd_place_count', 't_career_4th_place_or_below_count',
    't_career_turf_race_count', 't_career_turf_win_count',
    't_career_dirt_race_count', 't_career_dirt_win_count',
    't_career_1st_place_rate', 't_career_1st_2nd_place_rate',
    't_career_any_place_rate', 't_career_earnings'
]


class CombinedDateAttributesAdder(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        df = pd.DataFrame(X)
        df['h_age_days'] = (pd.to_datetime(df['r_date']) - pd.to_datetime(df['h_birthday'])).dt.days
        return df.drop(columns=['r_date', 'h_birthday']).values


class CombinedNumericAttributesAdder(BaseEstimator, TransformerMixin):
    def __init__(self):
        # passing 'num_attrs' via init is preferable, but 'not found' errors occurs in pipeline
        self.j_turf_wins_ix = num_attrs.index('j_career_turf_win_count')
        self.j_turf_races_ix = num_attrs.index('j_career_turf_race_count')
        self.j_dirt_wins_ix = num_attrs.index('j_career_dirt_win_count')
        self.j_dirt_races_ix = num_attrs.index('j_career_dirt_race_count')
        self.t_turf_wins_ix = num_attrs.index('t_career_turf_win_count')
        self.t_turf_races_ix = num_attrs.index('t_career_turf_race_count')
        self.t_dirt_wins_ix = num_attrs.index('t_career_dirt_win_count')
        self.t_dirt_races_ix = num_attrs.index('t_career_dirt_race_count')
        self.h_total_wins_ix = num_attrs.index('h_total_wins')
        self.h_total_races_ix = num_attrs.index('h_total_races')

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        j_turf_wins, j_turf_races = X[:, self.j_turf_wins_ix], X[:, self.j_turf_races_ix]
        j_turf_win_rate = np.divide(j_turf_wins, j_turf_races, out=np.zeros_like(j_turf_wins), where=j_turf_wins != 0.)

        j_dirt_wins, j_dirt_races = X[:, self.j_dirt_wins_ix], X[:, self.j_dirt_races_ix]
        j_dirt_win_rate = np.divide(j_dirt_wins, j_dirt_races, out=np.zeros_like(j_dirt_wins), where=j_dirt_wins != 0.)

        t_turf_wins, t_turf_races = X[:, self.t_turf_wins_ix], X[:, self.t_turf_races_ix]
        t_turf_win_rate = np.divide(t_turf_wins, t_turf_races, out=np.zeros_like(t_turf_wins), where=t_turf_wins != 0.)

        t_dirt_wins, t_dirt_races = X[:, self.t_dirt_wins_ix], X[:, self.t_dirt_races_ix]
        t_dirt_win_rate = np.divide(t_dirt_wins, t_dirt_races, out=np.zeros_like(t_dirt_wins), where=t_dirt_wins != 0.)

        h_wins, h_races = X[:, self.h_total_wins_ix], X[:, self.h_total_races_ix]
        h_win_rate = np.divide(h_wins, h_races, out=np.zeros_like(h_wins), where=h_wins != 0.)

        return np.c_[X, j_turf_win_rate, j_dirt_win_rate, t_turf_win_rate, t_dirt_win_rate, h_win_rate]


num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('num_attrs_adder', CombinedNumericAttributesAdder()),
    ('std_scaler', StandardScaler())
])

date_pipeline = Pipeline([
    ('date_attrs_adder', CombinedDateAttributesAdder()),
    ('imputer', SimpleImputer(strategy='median')),
    ('std_scaler', StandardScaler())
])

cat_pipeline = Pipeline([
    ('one_hot', OneHotEncoder(sparse=False, handle_unknown='ignore', categories=list(cat_attr_categories.values())))
])

full_pipeline = ColumnTransformer([
    ('num', num_pipeline, num_attrs),
    ('cat', cat_pipeline, list(cat_attr_categories.keys())),
    ('date', date_pipeline, date_attrs)
])
