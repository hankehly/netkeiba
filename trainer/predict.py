import argparse
import os
import sys

import pandas as pd

from sklearn.externals import joblib

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
from trainer.pipeline import full_pipeline, cat_attr_opts, bool_attrs, date_attributes, required_numeric_attributes


def read_data(data_path) -> pd.DataFrame:
    _, ext = os.path.splitext(data_path)

    if ext == '.json':
        df = pd.read_json(data_path, orient='records')
    elif ext == '.csv':
        df = pd.read_csv(data_path)
    else:
        raise ValueError(f'file extension ({ext}) not supported')

    # manual input needed for race
    df['r_weather'] = 'sunny'
    df['r_dirt_condition'] = 'good'
    df['r_turf_condition'] = 'good'

    # manual input needed per horse
    df['c_post_position'] = df.index + 1
    df['c_horse_weight'] = 99
    df['c_horse_weight_diff'] = 1

    return df[[
        *cat_attr_opts.keys(),
        *bool_attrs,
        *date_attributes,
        *required_numeric_attributes
    ]]


def main(data_path, model_path):
    X = read_data(data_path)
    X_prep = full_pipeline.fit_transform(X)
    model = joblib.load(model_path)
    predictions = model.predict(X_prep)
    X['estimated_norm_order_of_finish'] = predictions
    filename, _ = os.path.splitext(os.path.basename(data_path))
    pd.DataFrame(X).to_csv(f'pred_{filename}.csv')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data', type=str, help='location of unlabeled CSV data')
    parser.add_argument('model_path', type=str, help='location of joblib model')
    args = parser.parse_args()

    if not os.path.isfile(args.data):
        raise FileNotFoundError(f'data file does not exist: {args.data}')

    if not os.path.isfile(args.model_path):
        raise FileNotFoundError(f'model_path file does not exist: {args.model_path}')

    main(args.data, args.model_path)
