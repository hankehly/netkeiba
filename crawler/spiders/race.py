import re
from datetime import datetime

import scrapy
from bs4 import BeautifulSoup
from django.db import connection

from crawler.constants import RACETRACKS, COURSE_TYPES, IMPOST_CATEGORIES, HORSE_SEX
from crawler.parsers.horse import HorseParser
from crawler.parsers.jockey_result import JockeyResultParser
from crawler.parsers.trainer_result import TrainerResultParser


class TABLE_COL:
    POST_POS = 0
    HORSE = 3
    AGE_SEX = 4
    WEIGHT_CARRIED = 5
    JOCKEY = 6
    TRAINER = 7
    WEIGHT = 8
    ODDS = 9
    POPULARITY = 10


def _parse_post_position(row):
    return row.select('td')[TABLE_COL.POST_POS].string


def _parse_horse_weight(row):
    weight_col = row.select('td')[TABLE_COL.WEIGHT].string
    weight_search = re.search('([0-9]+)\(([+-]?[0-9]+)\)', weight_col)
    return int(weight_search.group(1)) if weight_search else None


def _parse_horse_weight_diff(row):
    weight_col = row.select('td')[TABLE_COL.WEIGHT].string
    weight_search = re.search('([0-9]+)\(([+-]?[0-9]+)\)', weight_col)
    return int(weight_search.group(2)) if weight_search else None


def _parse_horse_url(row):
    return row.select('td')[TABLE_COL.HORSE].select_one('a').get('href')


def _parse_horse_key(row):
    h_url = _parse_horse_url(row)
    return re.search('/horse/([0-9]+)', h_url).group(1)


def _prefix_keys(obj: dict, prefix: str):
    acc = {}
    for key, value in obj.items():
        pref_key = ''.join([prefix, key])
        acc[pref_key] = value
    return acc


def _parse_horse_sex(row):
    horse_sex_symbol = re.search('[^0-9]', row.select('td')[TABLE_COL.AGE_SEX].text).group()
    return HORSE_SEX.get(horse_sex_symbol)


def _parse_weight_carried(row):
    return float(row.select('td')[TABLE_COL.WEIGHT_CARRIED].text)


def _parse_jockey_key(row):
    jockey_column = row.select('td')[TABLE_COL.JOCKEY]
    if jockey_column.select_one('a[href]'):
        j_url = jockey_column.select_one('a').get('href')
        j_key = re.search('/jockey/([0-9]+)', j_url).group(1)
    else:
        j_key = ''
    return j_key


def _parse_trainer_key(row):
    t_url = row.select('td')[TABLE_COL.TRAINER].select_one('a').get('href')
    return re.search('/trainer/([0-9]+)', t_url).group(1)


def _parse_odds(row):
    return float(row.select('td')[TABLE_COL.ODDS].text)


def _parse_popularity(row):
    return int(row.select('td')[TABLE_COL.POPULARITY].text)


def _parse_previous_order_of_finish(row, date):
    h_key = _parse_horse_key(row)
    with connection.cursor() as cursor:
        previous_order_of_finish_query = '''
            SELECT c.order_of_finish
            FROM race_contenders c
                   LEFT JOIN races r ON c.race_id = r.id
            WHERE c.horse_id = (
              SELECT id
              FROM horses
              WHERE key = %s
              LIMIT 1
            )
              AND r.date < %s
            ORDER BY r.date DESC
            LIMIT 1
        '''
        result = cursor.execute(previous_order_of_finish_query, [h_key, date]).fetchone()
        return result[0] if result else None


class RaceSpider(scrapy.Spider):
    """
    scrapy crawl race -a race_url='https://race.netkeiba.com/?pid=race_old&id=xxx' -o xxx.jl
    """

    name = 'race'

    allowed_domains = ['race.netkeiba.com', 'db.netkeiba.com']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('race_url')]

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        contenders = soup.select_one('.race_table_old').select('tr.bml1')
        contender_count = len(contenders)

        racetrack = RACETRACKS.get(soup.select_one('.race_place a.active').text)
        date = datetime.strptime(re.search('[0-9]{4}/[0-9]{2}/[0-9]{2}', soup.title.text).group(), '%Y/%m/%d').date()
        race_dist_type_data = soup.select_one('.racedata').select_one('p:nth-of-type(1)').text
        race_dist_type_search = re.search('(.)([0-9]+)m', race_dist_type_data)
        course_type = COURSE_TYPES.get(race_dist_type_search.group(1))
        distance = int(race_dist_type_search.group(2))

        race_category_data = soup.select_one('.race_otherdata p:nth-of-type(2)').text

        impost_category = ''
        for key, val in IMPOST_CATEGORIES.items():
            if key in race_category_data:
                impost_category = val

        is_non_winner_regional_horse_allowed = 1 if '(指定)' in race_category_data else 0
        is_winner_regional_horse_allowed = 1 if '特指' in race_category_data else 0
        is_regional_jockey_allowed = 1 if '[指定]' in race_category_data else 0
        is_foreign_horse_allowed = 1 if '混' in race_category_data else 0
        is_foreign_horse_and_trainer_allowed = 1 if '国際' in race_category_data else 0
        is_apprentice_jockey_allowed = 1 if '見習騎手' in race_category_data else 0
        is_female_only = 1 if '牝' in race_category_data else 0

        race = {
            'contender_count': contender_count,
            'racetrack': racetrack,
            'date': date,
            'course_type': course_type,
            'distance': distance,
            'impost_category': impost_category,
            'is_non_winner_regional_horse_allowed': is_non_winner_regional_horse_allowed,
            'is_winner_regional_horse_allowed': is_winner_regional_horse_allowed,
            'is_regional_jockey_allowed': is_regional_jockey_allowed,
            'is_foreign_horse_allowed': is_foreign_horse_allowed,
            'is_foreign_horse_and_trainer_allowed': is_foreign_horse_and_trainer_allowed,
            'is_apprentice_jockey_allowed': is_apprentice_jockey_allowed,
            'is_female_only': is_female_only,
        }

        for row in contenders:
            c_post_position = _parse_post_position(row)
            h_url = _parse_horse_url(row)
            h_key = _parse_horse_key(row)
            h_sex = _parse_horse_sex(row)
            j_key = _parse_jockey_key(row)
            t_key = _parse_trainer_key(row)
            c_first_place_odds = _parse_odds(row)
            c_popularity = _parse_popularity(row)
            c_weight_carried = _parse_weight_carried(row)
            c_previous_order_of_finish = _parse_previous_order_of_finish(row, race['date'])
            c_horse_weight = _parse_horse_weight(row)
            c_horse_weight_diff = _parse_horse_weight_diff(row)

            meta = {
                'data': {
                    'c_post_position': c_post_position,
                    'h_key': h_key,
                    'h_sex': h_sex,
                    'j_key': j_key,
                    't_key': t_key,
                    'c_first_place_odds': c_first_place_odds,
                    'c_popularity': c_popularity,
                    'c_weight_carried': c_weight_carried,
                    'c_previous_order_of_finish': c_previous_order_of_finish,
                    'c_horse_weight': c_horse_weight,
                    'c_horse_weight_diff': c_horse_weight_diff,
                }
            }

            race_data = _prefix_keys(race, 'r_')
            meta['data'] = {**meta['data'], **race_data}

            yield scrapy.Request(h_url, callback=self.parse_horse, meta=meta, dont_filter=True)

    def parse_horse(self, response):
        parser = HorseParser(response.body)
        parser.parse()
        data = _prefix_keys(parser.data, 'h_')
        response.meta['data'] = {**response.meta['data'], **data}
        yield scrapy.Request(response.urljoin(f"/trainer/result/{response.meta['data']['t_key']}"),
                             callback=self.parse_trainer, meta=response.meta, dont_filter=True)

    def parse_trainer(self, response):
        parser = TrainerResultParser(response.body)
        parser.parse()
        data = _prefix_keys(parser.data, 't_')
        response.meta['data'] = {**response.meta['data'], **data}
        yield scrapy.Request(response.urljoin(f"/jockey/result/{response.meta['data']['j_key']}"),
                             callback=self.parse_jockey, meta=response.meta, dont_filter=True)

    def parse_jockey(self, response):
        parser = JockeyResultParser(response.body)
        parser.parse()
        data = _prefix_keys(parser.data, 'j_')
        yield {**response.meta['data'], **data}
