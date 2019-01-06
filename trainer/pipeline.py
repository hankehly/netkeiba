import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import MissingIndicator
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

"""
Numeric
"""

# TODO: Add 'c_actual_weight' (c_weight_carried + c_horse_weight)
# TODO: Add 'horse_class' or something similar (G1?) see chinese paper pg. 14
required_numeric_attributes = [
    'c_first_place_odds',
    'c_popularity',
    'c_post_position',
    'c_weight_carried',
    'h_total_races',
    'h_total_wins',
    'r_contender_count',
    'r_distance',
]

nullable_numeric_attributes = [
    'c_horse_weight',
    'c_horse_weight_diff',
    'c_previous_order_of_finish',
    'h_user_rating'
]


class NullableNumericTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, c_horse_weight=None, c_horse_weight_diff=None, c_previous_order_of_finish=None,
                 h_user_rating=None):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        null_rating_mask = X['h_user_rating'] == 0
        null_indices = X[null_rating_mask].index
        X.loc[null_indices, 'h_user_rating'] = np.nan

        # Ensure number of MissingIndicator features stays constant by specifying
        # features='all'. Variability in the number of columns causes a mismatch in
        # feature names and actual features.
        imputer_mask = MissingIndicator(features='all', sparse=False).fit_transform(X)

        # Impute the values manually because each value is handled differently
        mean_horse_weight = X['c_horse_weight'].mean()
        X['c_horse_weight'] = X['c_horse_weight'].fillna(mean_horse_weight)

        mean_horse_weight_diff = X['c_horse_weight_diff'].mean()
        X['c_horse_weight_diff'] = X['c_horse_weight_diff'].fillna(mean_horse_weight_diff)

        X['c_previous_order_of_finish'] = X['c_previous_order_of_finish'].fillna(0)
        X['h_user_rating'] = X['h_user_rating'].fillna(0)

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        return np.c_[X_scaled, imputer_mask]

    def get_feature_names(self):
        imputer_mask_attr_names = [f'{attr}_is_null' for attr in nullable_numeric_attributes]
        return nullable_numeric_attributes + imputer_mask_attr_names


nullable_numeric_transformer = NullableNumericTransformer()

"""
Categorical
"""

cat_attr_opts = {
    'h_sex': [
        'castrated',
        'female',
        'male'
    ],
    'r_course_type': [
        'dirt',
        'obstacle',
        'turf'
    ],
    'r_dirt_condition': [
        'bad',
        'good',
        'heavy',
        'slightly_heavy'
    ],
    'r_impost_category': [
        'age_based',
        'age_sex_based',
        'decided_per_race',
        'handicap'
    ],
    'r_racetrack': [
        'chukyo',
        'fuma',
        'hakodate',
        'hanshin',
        'kyoto',
        'nakayama',
        'niigata',
        'ogura',
        'sapporo',
        'tokyo'
    ],
    'r_turf_condition': [
        'bad',
        'good',
        'heavy',
        'slightly_heavy'
    ],
    'r_weather': [
        'cloudy',
        'rainy',
        'snowy',
        'sunny'
    ],
}

category_keys = list(cat_attr_opts.keys())
category_values = list(cat_attr_opts.values())
category_values_prefixed = [[f'{cat_key}_is_{value}' for value in cat_attr_opts[cat_key]] for cat_key in category_keys]

one_hot_encoder = OneHotEncoder(sparse=False, handle_unknown='ignore', categories=category_values)

"""
Date
"""

date_attributes = [
    'h_birthday',
    'r_date',
]


class HorseAgeAttributeAdder(BaseEstimator, TransformerMixin):
    def __init__(self, h_birthday=None, r_date=None):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        df = pd.DataFrame(X)
        df['h_age_days'] = (pd.to_datetime(df['r_date']) - pd.to_datetime(df['h_birthday'])).dt.days.astype(float)
        return df.drop(columns=['r_date', 'h_birthday']).values

    def get_feature_names(self):
        return ['h_age_days']


date_pipeline = Pipeline([
    ('horse_age_attribute_adder', HorseAgeAttributeAdder()),
    ('standard_scaler', StandardScaler())
])

"""
Boolean
"""

# TODO: Add 'is_day' attribute
bool_attrs = [
    'r_is_apprentice_jockey_allowed',
    'r_is_female_only',
    'r_is_foreign_horse_allowed',
    'r_is_foreign_horse_and_trainer_allowed',
    'r_is_non_winner_regional_horse_allowed',
    'r_is_regional_jockey_allowed',
    'r_is_winner_regional_horse_allowed',
]

full_pipeline = ColumnTransformer([
    ('required_numeric', StandardScaler(), required_numeric_attributes),
    ('nullable_numeric', nullable_numeric_transformer, nullable_numeric_attributes),
    ('categorical', one_hot_encoder, category_keys),
    ('date', date_pipeline, date_attributes),
    ('boolean', 'passthrough', bool_attrs),
], remainder='drop')

# TODO: Implement get_feature_names() in all transformers
# so that you can do the following by calling full_pipeline.get_feature_names()
full_pipeline_feature_names = np.hstack([
    # numeric
    required_numeric_attributes,

    # nullable numeric
    nullable_numeric_transformer.get_feature_names(),

    # categorical
    np.hstack(category_values_prefixed),

    # date
    date_pipeline.named_steps['horse_age_attribute_adder'].get_feature_names(),

    # boolean
    bool_attrs
])
