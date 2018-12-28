import os
import sys
from datetime import datetime

import numpy as np
from sklearn.externals import joblib
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import StratifiedShuffleSplit

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
from trainer.pipeline import full_pipeline
from trainer.model import train_rand_forest_reg_random_search
from src.utils import read_netkeiba

np.random.seed(42)

df = read_netkeiba()

df['r_contender_count'] = df.groupby('r_id').c_id.count().loc[df.r_id].values
df['c_norm_order_of_finish'] = 1.0 - (df.c_order_of_finish - 1) / (df.r_contender_count - 1)

index_attrs = ['c_id', 'r_id', 'h_id', 'j_id', 't_id', 'r_key', 'h_key', 'j_key', 't_key']
label_attrs = ['c_norm_order_of_finish', 'c_order_of_finish', 'c_finish_time', 'c_order_of_finish_lowered']

X = df.drop(columns=index_attrs + label_attrs)
y = df.c_norm_order_of_finish

sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
approx_y = round(y, 1)

for train_idx, test_idx in sss.split(X, approx_y):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

X_train_prep = full_pipeline.fit_transform(X_train)
model = train_rand_forest_reg_random_search(X_train_prep, y_train)

predictions = model.predict(X_train_prep)

rmse = np.sqrt(mean_squared_error(y_train, predictions))
mae = mean_absolute_error(y_train, predictions)

timestamp = datetime.now().isoformat(timespec='minutes').replace(':', '')
dirname = os.path.join(PROJECT_ROOT, 'tmp', 'models', f'rand_forest_reg_{timestamp}')
os.mkdir(dirname)

joblib.dump(model, os.path.join(dirname, 'model.joblib'))
joblib.dump(X_train, os.path.join(dirname, 'X_train.joblib'))
joblib.dump(y_train, os.path.join(dirname, 'y_train.joblib'))
joblib.dump(X_test, os.path.join(dirname, 'X_test.joblib'))
joblib.dump(y_test, os.path.join(dirname, 'y_test.joblib'))

with open(os.path.join(dirname, 'results.txt'), 'w') as f:
    f.write(f'# {dirname}\n')
    f.write(f'RMSE: {rmse}\n')
    f.write(f'MAE: {mae}\n')

print(f'Exported to {dirname}')
