import logging
import os
import sys

from sklearn.model_selection import StratifiedShuffleSplit

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
from scripts.utils import read_netkeiba
from trainer.pipeline import full_pipeline

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


def main():
    """
    Model Preparation
    """
    df = read_netkeiba()

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

    full_pipeline.fit_transform(X_train)
    logging.debug('finished')


if __name__ == '__main__':
    main()
