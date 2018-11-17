import os
import sqlite3

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def main():
    conn = sqlite3.connect(os.path.join(PROJECT_ROOT, 'netkeiba.sqlite'))
    c = conn.cursor()
    with open(os.path.join(PROJECT_ROOT, 'scripts', 'create_db.sql'), 'r') as f:
        sql = f.read()
        c.executescript(sql)


if __name__ == '__main__':
    main()
