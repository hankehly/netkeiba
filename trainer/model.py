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
