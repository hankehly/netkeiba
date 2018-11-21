import os
import sqlite3

import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def read_netkeiba():
    conn = sqlite3.connect(os.path.join(PROJECT_ROOT, 'netkeiba.sqlite'))
    cur = conn.cursor()

    with open(os.path.join(PROJECT_ROOT, 'scripts', 'select_all.sql'), 'r') as f:
        rows = cur.execute(f.read()).fetchall()

        # Get the column names of the last query. To remain compatible with the Python DB API,
        # it returns a 7-tuple for each column where the last six items of each tuple are None.
        cols = [desc[0] for desc in cur.description]

        return pd.DataFrame(rows, columns=cols)
