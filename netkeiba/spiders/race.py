import re
from datetime import datetime, time

import pytz
import scrapy
from bs4 import BeautifulSoup
from django.db import connection

from netkeiba.parsers.race import RACETRACKS, SURFACES, IMPOST_CATEGORIES, HORSE_SEX, WEATHER


class TABLE_COL:
    POST_POS = 0
    HORSE_NUM = 1
    HORSE = 3
    AGE_SEX = 4
    WEIGHT_CARRIED = 5
    JOCKEY = 6
    TRAINER = 7
    WEIGHT = 8
    ODDS = 9
    POPULARITY = 10


def _parse_racetrack(soup):
    return RACETRACKS.get(soup.select_one('.race_place a.active').text)


def _parse_datetime(soup):
    race_date = datetime.strptime(re.search('[0-9]{4}/[0-9]{2}/[0-9]{2}', soup.title.text).group(), '%Y/%m/%d').date()
    track_details = _parse_track_details(soup)
    time_str = re.search('[0-9]{2}:[0-9]{2}', track_details[-1]).group()
    hours, minutes = list(map(int, time_str.split(':')))
    race_time = time(hours, minutes)
    jst = pytz.timezone('Asia/Tokyo')
    dt = datetime.combine(race_date, race_time)
    return jst.localize(dt)


def _parse_track_details(soup):
    return soup.select_one('.racedata').select_one('p:nth-of-type(2)').text \
        .replace(u'\xa0', u'').replace(' ', '').split('/')


def _parse_course_type(soup):
    race_dist_type_data = soup.select_one('.racedata').select_one('p:nth-of-type(1)').text
    race_dist_type_search = re.search('(.)([0-9]+)m', race_dist_type_data)
    return SURFACES.get(race_dist_type_search.group(1))


def _parse_distance(soup):
    race_dist_type_data = soup.select_one('.racedata').select_one('p:nth-of-type(1)').text
    race_dist_type_search = re.search('(.)([0-9]+)m', race_dist_type_data)
    return int(race_dist_type_search.group(2))


def _parse_weather(soup):
    track_details = _parse_track_details(soup)
    weather = None
    for key, val in WEATHER.items():
        if key in track_details[0]:
            weather = val
    return weather


def _parse_track_condition(soup):
    track_details = _parse_track_details(soup)
    condition = None
    if '良' in track_details[1]:
        condition = 'good'
    elif '稍重' in track_details[1]:
        condition = 'slightly_heavy'
    elif '重' in track_details[1]:
        condition = 'heavy'
    elif '不良' in track_details[1]:
        condition = 'bad'
    return condition


def _parse_dirt_condition(soup):
    course_type = _parse_course_type(soup)
    if course_type == 'dirt':
        return _parse_track_condition(soup)
    return ''


def _parse_turf_condition(soup):
    course_type = _parse_course_type(soup)
    if course_type == 'turf':
        return _parse_track_condition(soup)
    return ''


def _parse_impost_category(soup):
    race_category_data = soup.select_one('.race_otherdata p:nth-of-type(2)').text
    for key, val in IMPOST_CATEGORIES.items():
        if key in race_category_data:
            return val
    return ''


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


def _parse_horse_number(row):
    return int(row.select('td')[TABLE_COL.HORSE_NUM].string)


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


def _parse_previous_order_of_finish(row, dt):
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
              AND r.datetime < %s
            ORDER BY r.datetime DESC
            LIMIT 1
        '''
        result = cursor.execute(previous_order_of_finish_query, [h_key, dt]).fetchone()
        return result[0] if result else None


class RaceSpider(scrapy.Spider):
    name = 'race'

    allowed_domains = ['db.netkeiba.com']

    def __init__(self, race_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [race_url]
        self.logger.info(f'race_url set to {race_url}')

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        contenders = soup.select_one('.race_table_old').select('tr.bml1')
        contender_count = len(contenders)
        racetrack = _parse_racetrack(soup)
        datetime = _parse_datetime(soup)
        course_type = _parse_course_type(soup)
        distance = _parse_distance(soup)
        weather = _parse_weather(soup)
        dirt_condition = _parse_dirt_condition(soup)
        turf_condition = _parse_turf_condition(soup)
        impost_category = _parse_impost_category(soup)

        race_category_data = soup.select_one('.race_otherdata p:nth-of-type(2)').text
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
            'datetime': datetime,
            'course_type': course_type,
            'distance': distance,
            'weather': weather,
            'dirt_condition': dirt_condition,
            'turf_condition': turf_condition,
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
            c_previous_order_of_finish = _parse_previous_order_of_finish(row, race['datetime'])
            c_horse_weight = _parse_horse_weight(row)
            c_horse_weight_diff = _parse_horse_weight_diff(row)
            c_horse_number = _parse_horse_number(row)

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
                    'c_horse_number': c_horse_number,
                }
            }

            race_data = _prefix_keys(race, 'r_')
            meta['data'] = {**meta['data'], **race_data}
            yield {**meta['data'], **race_data}
