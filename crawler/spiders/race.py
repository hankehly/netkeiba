import re
from datetime import datetime

import scrapy
from bs4 import BeautifulSoup
from django.db import connection

from crawler.constants import RACETRACKS, COURSE_TYPES, IMPOST_CATEGORIES, HORSE_SEX
from crawler.parsers.horse import HorseParser
from crawler.parsers.jockey_result import JockeyResultParser
from crawler.parsers.trainer_result import TrainerResultParser


def _prefix_keys(obj: dict, prefix: str):
    acc = {}
    for key, value in obj.items():
        pref_key = ''.join([prefix, key])
        acc[pref_key] = value
    return acc


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
            h_url = row.select('td')[1].select_one('a').get('href')
            h_key = re.search('/horse/([0-9]+)', h_url).group(1)
            horse_sex_symbol = re.search('[^0-9]', row.select('td')[2].text).group()
            h_sex = HORSE_SEX.get(horse_sex_symbol)
            c_weight_carried = float(row.select('td')[3].text)

            jockey_column = row.select('td')[4]
            if jockey_column.select_one('a[href]'):
                j_url = jockey_column.select_one('a').get('href')
                j_key = re.search('/jockey/([0-9]+)', j_url).group(1)
            else:
                j_key = ''

            t_url = row.select('td')[5].select_one('a').get('href')
            t_key = re.search('/trainer/([0-9]+)', t_url).group(1)
            c_first_place_odds = float(row.select('td')[6].text)
            c_popularity = int(row.select('td')[7].text)

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
                result = cursor.execute(previous_order_of_finish_query, [h_key, race['date']]).fetchone()
                c_previous_order_of_finish = result[0] if result else None

            meta = {
                'data': {
                    'h_key': h_key,
                    'h_sex': h_sex,
                    'j_key': j_key,
                    't_key': t_key,
                    'c_first_place_odds': c_first_place_odds,
                    'c_popularity': c_popularity,
                    'c_weight_carried': c_weight_carried,
                    'c_previous_order_of_finish': c_previous_order_of_finish,
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
