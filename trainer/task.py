import os
import sys

import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
from trainer.pipeline import full_pipeline
from trainer.model import train_rand_forest_reg_random_search
from trainer.util import read_netkeiba, upload_model

np.random.seed(42)

X, y = read_netkeiba()

sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

for train_idx, test_idx in sss.split(X, y):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

X_train_prep = full_pipeline.fit_transform(X_train)
model = train_rand_forest_reg_random_search(X_train_prep, y_train)
upload_model(model)
