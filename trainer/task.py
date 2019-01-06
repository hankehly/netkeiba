import os
import sys

import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
from trainer.pipeline import full_pipeline
from trainer.model import train_random_forest_regressor_random_search
from trainer.util import read_netkeiba, upload_model_with_results, split_train_test

np.random.seed(42)

X, y = read_netkeiba()
X_train, X_test, y_train, y_test = split_train_test(X, y)
X_train_prep = full_pipeline.fit_transform(X_train)
model = train_random_forest_regressor_random_search(X_train_prep, y_train)
upload_model_with_results(model, X_test, y_test)
