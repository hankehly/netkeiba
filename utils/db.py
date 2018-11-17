import os
import sqlite3

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def create_tables():
    conn = sqlite3.connect(os.path.join(PROJECT_ROOT, 'utils', 'netkeiba.sqlite'))
    c = conn.cursor()
    with open(os.path.join(PROJECT_ROOT, 'utils', 'create_tables.sql'), 'r') as f:
        sql = f.read()
        c.executescript(sql)
