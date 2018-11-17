import argparse
import os
import sqlite3

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def create_db(overwrite=False):
    db_file = os.path.join(PROJECT_ROOT, 'netkeiba.sqlite')
    if overwrite and os.path.isfile(db_file):
        os.remove(db_file)
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    with open(os.path.join(PROJECT_ROOT, 'scripts', 'create_db.sql'), 'r') as f:
        sql = f.read()
        c.executescript(sql)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--force', action='store_true', help='overwrite current database if exists')
    args = parser.parse_args()
    create_db(args.force)
