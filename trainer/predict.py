import argparse
import os
import sys

import numpy as np
import pandas as pd

from sklearn.externals import joblib
from tabulate import tabulate

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
from trainer.pipeline import full_pipeline, category_keys, bool_attrs, date_attributes, required_numeric_attributes, \
    nullable_numeric_attributes


def read_data(data_path) -> pd.DataFrame:
    _, ext = os.path.splitext(data_path)

    if ext == '.json':
        df = pd.read_json(data_path, orient='records')
    elif ext == '.csv':
        df = pd.read_csv(data_path)
    else:
        raise ValueError(f'file extension ({ext}) unsupported')

    # TODO: Manual input needed
    df['r_weather'] = 'sunny'
    df['c_post_position'] = df.index + 1
    df['r_dirt_condition'] = None
    df['r_turf_condition'] = None
    df['c_horse_weight'] = 0
    df['c_horse_weight_diff'] = 0

    attrs = np.hstack([
        category_keys,
        bool_attrs,
        date_attributes,
        required_numeric_attributes,
        nullable_numeric_attributes,
        'h_key'
    ])

    return df[attrs]


def main(data_path, model_path):
    X_train = read_data(data_path)
    X_out = X_train.copy()[['h_key', 'c_first_place_odds', 'c_popularity']]
    X_out['h_key'] = X_out['h_key'].astype(str)

    X_train.drop(columns=['h_key'], inplace=True)
    X_train_prep = full_pipeline.fit_transform(X_train)

    estimator = joblib.load(model_path)
    predictions = estimator.predict(X_train_prep)
    X_out['c_meters_per_second'] = predictions
    X_out.sort_values(by='c_meters_per_second', inplace=True)

    filename, _ = os.path.splitext(os.path.basename(data_path))
    with open(f'pred_{filename}.txt', 'w') as fh:
        print(tabulate(X_out, headers='keys', tablefmt='pipe'), file=fh)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data', type=str, help='location of unlabeled data')
    parser.add_argument('model_path', type=str, help='location of joblib model')
    args = parser.parse_args()

    if not os.path.isfile(args.data):
        raise FileNotFoundError(f'data file does not exist: {args.data}')

    if not os.path.isfile(args.model_path):
        raise FileNotFoundError(f'model_path file does not exist: {args.model_path}')

    main(args.data, args.model_path)
