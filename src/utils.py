import os
import sqlite3

import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def read_netkeiba():
    conn = sqlite3.connect(os.path.join(PROJECT_ROOT, 'db.sqlite3'))
    cur = conn.cursor()

    with open(os.path.join(PROJECT_ROOT, 'src', 'select_all.sql'), 'r') as f:
        rows = cur.execute(f.read()).fetchall()

        # Get the column names of the last query. To remain compatible with the Python DB API,
        # it returns a 7-tuple for each column where the last six items of each tuple are None.
        cols = [desc[0] for desc in cur.description]

        df = pd.DataFrame(rows, columns=cols)

        df['r_contender_count'] = df.groupby('r_id').c_id.count().loc[df.r_id].values
        df['c_meters_per_second'] = (df['c_finish_time'] / df['r_distance']).round(6)

        label_value_counts = df['c_meters_per_second'].value_counts()
        stray_label_values = label_value_counts.index[label_value_counts < 2].values
        stray_label_bool_mask = df['c_meters_per_second'].isin(stray_label_values)
        stray_label_indices = df[stray_label_bool_mask].index
        df.drop(stray_label_indices, inplace=True)

        # df['is_day'] = None
        # df['h_old_place'] = None

        index_attrs = ['c_id', 'r_id', 'h_id', 'j_id', 't_id', 'r_key', 'h_key', 'j_key', 't_key']
        label_attrs = ['c_order_of_finish', 'c_finish_time', 'c_order_of_finish_lowered', 'c_meters_per_second']

        X = df.drop(columns=index_attrs + label_attrs)
        y = df['c_meters_per_second']

        return X, y
