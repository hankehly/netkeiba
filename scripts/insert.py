import argparse
import json
import logging
import os
import sqlite3

from bs4 import BeautifulSoup

from create_db import create_db

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

logging.basicConfig(
    filename=os.path.join(PROJECT_ROOT, 'scripts', 'insert.log'),
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

logger = logging.getLogger(__name__)


class Persistor:
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(PROJECT_ROOT, 'netkeiba.sqlite'))

    def create_or_update(self, table_name: str, item_key: str, **kwargs):
        logger.debug(f'[create_or_update] {table_name} {item_key}')

        keys = ','.join(['key'] + [str(v) for v in list(kwargs.keys())])
        vals = ','.join([item_key] + [str(v) for v in list(kwargs.values())])

        try:
            with self.conn:
                self.conn.execute(f'INSERT INTO {table_name} ({keys}) VALUES ({vals});')
        except sqlite3.IntegrityError as e:
            logger.debug(f'[Persistor.create_or_update] {e} (table: {table_name}, item_key: {item_key})')


class Parser:
    def __init__(self, persistor: Persistor):
        self.persistor = persistor

    def parse_item(self, item: dict):
        handlers = {'race': self.parse_race_item, 'horse': self.parse_horse_item, 'jockey': self.parse_jockey_item,
                    'trainer': self.parse_trainer_item}

        handlers.get(item['item_type'], self.noop)(item)

    def str2float(self, value: str) -> float:
        return float(value.replace(',', ''))

    def str2int(self, value: str) -> int:
        return int(value.replace(',', ''))

    def parse_trainer_item(self, item: dict):
        logger.debug(f"[Parser.parse_trainer_item] {item['id']}")

        soup = BeautifulSoup(item['response_body'], 'html.parser')
        agg_data = soup.select_one('.race_table_01 tr:nth-of-type(3)')

        try:
            career_1st_place_count = self.str2int(agg_data.select_one('td:nth-of-type(3) a').string)
            career_2nd_place_count = self.str2int(agg_data.select_one('td:nth-of-type(4) a').string)
            career_3rd_place_count = self.str2int(agg_data.select_one('td:nth-of-type(5) a').string)
            career_4th_place_or_below_count = self.str2int(agg_data.select_one('td:nth-of-type(6) a').string)
            career_turf_race_count = self.str2int(agg_data.select_one('td:nth-of-type(13) a').string)
            career_turf_win_count = self.str2int(agg_data.select_one('td:nth-of-type(14) a').string)
            career_dirt_race_count = self.str2int(agg_data.select_one('td:nth-of-type(15) a').string)
            career_dirt_win_count = self.str2int(agg_data.select_one('td:nth-of-type(16) a').string)
            career_1st_place_rate = self.str2float(agg_data.select_one('td:nth-of-type(17)').string)
            career_1st_2nd_place_rate = self.str2float(agg_data.select_one('td:nth-of-type(18)').string)
            career_any_place_rate = self.str2float(agg_data.select_one('td:nth-of-type(19)').string)
            career_earnings = self.str2float(agg_data.select_one('td:nth-of-type(20)').string)
        except AttributeError as e:
            logger.debug(f"{e} - {item['url']}")
        else:
            self.persistor.create_or_update(
                'trainers',
                item['id'],
                career_1st_place_count=career_1st_place_count,
                career_2nd_place_count=career_2nd_place_count,
                career_3rd_place_count=career_3rd_place_count,
                career_4th_place_or_below_count=career_4th_place_or_below_count,
                career_turf_race_count=career_turf_race_count,
                career_turf_win_count=career_turf_win_count,
                career_dirt_race_count=career_dirt_race_count,
                career_dirt_win_count=career_dirt_win_count,
                career_1st_place_rate=career_1st_place_rate,
                career_1st_2nd_place_rate=career_1st_2nd_place_rate,
                career_any_place_rate=career_any_place_rate,
                career_earnings=career_earnings,
                url=f"'{item['url']}'"
            )

    def parse_jockey_item(self, item: dict):
        logger.debug(f"[Parser.parse_jockey_item] {item['id']}")

        soup = BeautifulSoup(item['response_body'], 'html.parser')
        agg_data = soup.select_one('.race_table_01 tr:nth-of-type(3)')

        try:
            career_1st_place_count = self.str2int(agg_data.select_one('td:nth-of-type(3) a').string)
            career_2nd_place_count = self.str2int(agg_data.select_one('td:nth-of-type(4) a').string)
            career_3rd_place_count = self.str2int(agg_data.select_one('td:nth-of-type(5) a').string)
            career_4th_place_or_below_count = self.str2int(agg_data.select_one('td:nth-of-type(6) a').string)
            career_turf_race_count = self.str2int(agg_data.select_one('td:nth-of-type(13) a').string)
            career_turf_win_count = self.str2int(agg_data.select_one('td:nth-of-type(14) a').string)
            career_dirt_race_count = self.str2int(agg_data.select_one('td:nth-of-type(15) a').string)
            career_dirt_win_count = self.str2int(agg_data.select_one('td:nth-of-type(16) a').string)
            career_1st_place_rate = self.str2float(agg_data.select_one('td:nth-of-type(17)').string)
            career_1st_2nd_place_rate = self.str2float(agg_data.select_one('td:nth-of-type(18)').string)
            career_any_place_rate = self.str2float(agg_data.select_one('td:nth-of-type(19)').string)
            career_earnings = self.str2float(agg_data.select_one('td:nth-of-type(20)').string)
        except AttributeError as e:
            logger.debug(f"{e} - {item['url']}")
        else:
            self.persistor.create_or_update(
                'jockeys',
                item['id'],
                career_1st_place_count=career_1st_place_count,
                career_2nd_place_count=career_2nd_place_count,
                career_3rd_place_count=career_3rd_place_count,
                career_4th_place_or_below_count=career_4th_place_or_below_count,
                career_turf_race_count=career_turf_race_count,
                career_turf_win_count=career_turf_win_count,
                career_dirt_race_count=career_dirt_race_count,
                career_dirt_win_count=career_dirt_win_count,
                career_1st_place_rate=career_1st_place_rate,
                career_1st_2nd_place_rate=career_1st_2nd_place_rate,
                career_any_place_rate=career_any_place_rate,
                career_earnings=career_earnings,
                url=f"'{item['url']}'"
            )

    def parse_horse_item(self, item: dict):
        logger.debug(f"[Parser.parse_horse_item] {item['id']}")

    def parse_race_item(self, item: dict):
        logger.debug(f"[Parser.parse_race_item] {item['id']}")

    def noop(item):
        logger.debug(f"[Parser.noop] {vars(item)}")


def main(opts):
    if not os.path.isfile(opts.input):
        raise FileNotFoundError(f'input file does not exist: {opts.input}')

    if opts.reset:
        logger.debug('Dropping and rebuilding database')
        create_db(overwrite=True)

    persistor = Persistor()
    parser = Parser(persistor)

    logger.debug('Parsing started')

    with open(opts.input, 'r') as f:
        for obj in f:
            parser.parse_item(json.loads(obj))

    logger.debug('Parsing finished')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='file containing scraped data')
    parser.add_argument('--reset', action='store_true', help='drop and recreate the database before insertion')
    args = parser.parse_args()
    main(args)
