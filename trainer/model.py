import logging
import numpy as np
import os
import pandas as pd
import sys
from datetime import datetime

from scipy.stats import randint
from sklearn.ensemble import RandomForestRegressor
from sklearn.externals import joblib
from sklearn.linear_model import SGDRegressor
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

np.random.seed(42)


def get_timestamp():
    return datetime.now().isoformat(timespec='minutes').replace(':', '')


def train_forest_random_search(X_train_prep, y_train):
    param_distributions = {
        'n_estimators': randint(low=1, high=200),
        'max_features': randint(low=1, high=8),
    }

    forest_reg = RandomForestRegressor(random_state=42)
    rand_search = RandomizedSearchCV(forest_reg, param_distributions=param_distributions, n_iter=25, cv=5,
                                     scoring='neg_mean_squared_error', random_state=42, verbose=5, n_jobs=-1)

    rand_search.fit(X_train_prep, y_train)

    timestamp = get_timestamp()
    filename = f'forest_reg_{timestamp}.gz'
    joblib.dump(rand_search, filename)

    logging.info(f'Training complete. Output {filename}')


def train_sgd_regressor_grid_search(X_train_prep, y_train):
    param_grid = {
        'alpha': 10.0 ** -np.arange(1, 7),
        'loss': ['squared_loss', 'huber', 'epsilon_insensitive'],
        'penalty': ['l2', 'l1', 'elasticnet'],
        'learning_rate': ['constant', 'optimal', 'invscaling'],
    }

    sgd_reg = SGDRegressor(random_state=42)
    grid_search = GridSearchCV(sgd_reg, param_grid, n_jobs=-1, verbose=5, cv=5)
    grid_search.fit(X_train_prep, y_train)

    timestamp = get_timestamp()
    filename = f'sgd_reg_{timestamp}.gz'
    joblib.dump(grid_search, filename)

    logging.info(f'Training complete. Output {filename}')
