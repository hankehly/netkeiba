import logging

import numpy as np
import os
import sys
from datetime import datetime

from scipy.stats import randint
from sklearn.ensemble import RandomForestRegressor
from sklearn.externals import joblib
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
from trainer.pipeline import full_pipeline

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

np.random.seed(42)


def get_timestamp():
    return datetime.now().isoformat(timespec='minutes').replace(':', '')


def train_rand_forest_reg_random_search(X_train, X_test, y_train, y_test):
    X_train_prep = full_pipeline.fit_transform(X_train)

    param_distributions = {
        'n_estimators': randint(low=1, high=200),
        'max_features': randint(low=1, high=8),
    }

    rand_forest_reg = RandomForestRegressor(random_state=42)
    rand_search = RandomizedSearchCV(rand_forest_reg, param_distributions=param_distributions, n_iter=25, cv=5,
                                     scoring='neg_mean_squared_error', random_state=42, verbose=5, n_jobs=-1)
    rand_search.fit(X_train_prep, y_train)
    export_results(rand_search, X_test, y_test, 'rand_forest_reg')
    logger.info(f'Training complete')


def train_sgd_regressor_grid_search(X_train, X_test, y_train, y_test):
    X_train_prep = full_pipeline.fit_transform(X_train)

    param_grid = {
        'alpha': 10.0 ** -np.arange(1, 7),
        'loss': ['squared_loss', 'huber', 'epsilon_insensitive'],
        'penalty': ['l2', 'l1', 'elasticnet'],
        'learning_rate': ['constant', 'optimal', 'invscaling'],
    }

    sgd_reg = SGDRegressor(random_state=42)
    grid_search = GridSearchCV(sgd_reg, param_grid, n_jobs=-1, verbose=5, cv=5)
    grid_search.fit(X_train_prep, y_train)
    export_results(grid_search, X_test, y_test, 'sgd_reg')
    logger.info(f'Training complete')


# TODO: This should be a separate step from the training script
# Add to end of task.py instead
def export_results(model, X_test, y_test, prefix):
    X_test_prep = full_pipeline.fit_transform(X_test)
    predictions = model.predict(X_test_prep)

    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, predictions)

    timestamp = get_timestamp()
    dirname = f'{prefix}_{timestamp}'

    os.mkdir(dirname)

    joblib.dump(model, os.path.join(dirname, 'model.gz'))
    joblib.dump(X_test, os.path.join(dirname, 'X_test.gz'))
    joblib.dump(y_test, os.path.join(dirname, 'y_test.gz'))

    with open(os.path.join(dirname, 'results.txt'), 'w') as f:
        f.write(f'# {dirname}\n')
        f.write(f'RMSE: {rmse}\n')
        f.write(f'MAE: {mae}\n')

    logger.info(f'Exported to {dirname}')
