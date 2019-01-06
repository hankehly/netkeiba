import numpy as np

from scipy.stats import randint
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import SGDRegressor
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

np.random.seed(42)


def train_random_forest_regressor_random_search(X_train_prep, y_train):
    param_distributions = {
        'n_estimators': randint(low=1, high=200),
        'max_features': randint(low=1, high=8),
    }

    rand_forest_reg = RandomForestRegressor(random_state=42)
    rand_search = RandomizedSearchCV(rand_forest_reg, param_distributions=param_distributions, n_iter=25, cv=5,
                                     scoring='neg_mean_squared_error', random_state=42, verbose=5, n_jobs=-1)
    rand_search.fit(X_train_prep, y_train)
    print('Training complete')

    return rand_search.best_estimator_


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
    print('Training complete')

    return grid_search
