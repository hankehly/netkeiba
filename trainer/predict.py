import argparse
import os
import pandas as pd

from sklearn.externals import joblib

from trainer.pipeline import full_pipeline


def main(csv_path, model_path):
    X = pd.read_csv(csv_path)
    X_prep = full_pipeline.fit_transform(X)
    model = joblib.load(model_path)
    predictions = model.predict(X_prep)
    pd.DataFrame(predictions).to_csv('predictions.csv')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data', type=str, help='location of unlabeled CSV data')
    parser.add_argument('model_path', str, help='location of joblib model')
    args = parser.parse_args()

    if not os.path.isfile(args.data):
        raise FileNotFoundError(f'data file does not exist: {args.data}')

    if not os.path.isfile(args.model_path):
        raise FileNotFoundError(f'model_path file does not exist: {args.model_path}')

    main(args.data, args.model_path)
