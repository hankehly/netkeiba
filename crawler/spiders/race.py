import re
from datetime import datetime

import scrapy
from bs4 import BeautifulSoup

from crawler.parsers.horse import HorseParser
from crawler.parsers.jockey_result import JockeyResultParser
from crawler.parsers.trainer_result import TrainerResultParser

RACETRACKS = {
    '札幌': 'sapporo',
    '函館': 'hakodate',
    '福島': 'fuma',
    '新潟': 'niigata',
    '東京': 'tokyo',
    '中山': 'nakayama',
    '中京': 'chukyo',
    '京都': 'kyoto',
    '阪神': 'hanshin',
    '小倉': 'ogura'
}

WEATHER = {
    '曇': 'cloudy',
    '晴': 'sunny',
    '雨': 'rainy',
    '雪': 'snowy',
}

IMPOST_CATEGORIES = {
    '馬齢': 'age_based',
    '定量': 'age_sex_based',
    '別定': 'decided_per_race',
    'ハンデ': 'handicap'
}

COURSE_TYPES = {
    '芝': 'turf',
    'ダ': 'dirt',
    '障': 'obstacle'
}

HORSE_SEX = {
    '牝': 'female',
    '牡': 'male',
    'セ': 'castrated'
}


class RaceSpider(scrapy.Spider):
    """
    scrapy crawl race -a race_url='https://race.netkeiba.com/?pid=race_old&id=xxx' -o xxx.csv
    """
    name = 'race'
    allowed_domains = ['race.netkeiba.com', 'db.netkeiba.com']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('race_url')]

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        contenders = soup.select_one('.race_table_old').select('tr.bml1')
        r_contender_count = len(contenders)

        r_racetrack = RACETRACKS.get(soup.select_one('.race_place a.active').text)
        r_date = datetime.strptime(re.search('[0-9]{4}/[0-9]{2}/[0-9]{2}', soup.title.text).group(), '%Y/%m/%d').date()
        race_dist_type_data = soup.select_one('.racedata').select_one('p:nth-of-type(1)').text
        race_dist_type_search = re.search('(.)([0-9]+)m', race_dist_type_data)
        r_course_type = COURSE_TYPES.get(race_dist_type_search.group(1))
        r_distance = int(race_dist_type_search.group(2))

        race_category_data = soup.select_one('.race_otherdata p:nth-of-type(2)').text

        r_impost_category = ''
        for key, val in IMPOST_CATEGORIES.items():
            if key in race_category_data:
                r_impost_category = val

        r_is_non_winner_regional_horse_allowed = 1 if '(指定)' in race_category_data else 0
        r_is_winner_regional_horse_allowed = 1 if '特指' in race_category_data else 0
        r_is_regional_jockey_allowed = 1 if '[指定]' in race_category_data else 0
        r_is_foreign_horse_allowed = 1 if '混' in race_category_data else 0
        r_is_foreign_horse_and_trainer_allowed = 1 if '国際' in race_category_data else 0
        r_is_apprentice_jockey_allowed = 1 if '見習騎手' in race_category_data else 0
        r_is_female_only = 1 if '牝' in race_category_data else 0

        race = {
            'r_contender_count': r_contender_count,
            'r_racetrack': r_racetrack,
            'r_date': r_date,
            'r_course_type': r_course_type,
            'r_distance': r_distance,
            'r_impost_category': r_impost_category,
            'r_is_non_winner_regional_horse_allowed': r_is_non_winner_regional_horse_allowed,
            'r_is_winner_regional_horse_allowed': r_is_winner_regional_horse_allowed,
            'r_is_regional_jockey_allowed': r_is_regional_jockey_allowed,
            'r_is_foreign_horse_allowed': r_is_foreign_horse_allowed,
            'r_is_foreign_horse_and_trainer_allowed': r_is_foreign_horse_and_trainer_allowed,
            'r_is_apprentice_jockey_allowed': r_is_apprentice_jockey_allowed,
            'r_is_female_only': r_is_female_only,
        }

        for row in contenders:
            h_url = row.select('td')[1].select_one('a').get('href')
            h_key = re.search('/horse/([0-9]+)', h_url).group(1)
            horse_sex_symbol = re.search('[^0-9]', row.select('td')[2].text).group()
            h_sex = HORSE_SEX.get(horse_sex_symbol)
            c_weight_carried = float(row.select('td')[3].text)

            jockey_column = row.select('td')[4]
            if jockey_column.select_one("a['href']"):
                j_url = jockey_column.select_one('a').get('href')
                j_key = re.search('/jockey/([0-9]+)', j_url).group(1)
            else:
                j_key = ''

            t_url = row.select('td')[5].select_one('a').get('href')
            t_key = re.search('/trainer/([0-9]+)', t_url).group(1)
            c_first_place_odds = float(row.select('td')[6].text)
            c_popularity = int(row.select('td')[7].text)

            meta = {
                'data': {
                    'h_key': h_key,
                    'h_sex': h_sex,
                    'j_key': j_key,
                    't_key': t_key,
                    'c_first_place_odds': c_first_place_odds,
                    'c_popularity': c_popularity,
                    'c_weight_carried': c_weight_carried
                }
            }

            meta['data'] = {**meta['data'], **race}

            yield scrapy.Request(h_url, callback=self.parse_horse, meta=meta, dont_filter=True)

    def parse_horse(self, response):
        horse_data = HorseParser(response.body).parse()
        response.meta['data'] = {**response.meta['data'], **horse_data}
        yield scrapy.Request(response.urljoin(f"/trainer/result/{response.meta['data']['t_key']}"),
                             callback=self.parse_trainer, meta=response.meta, dont_filter=True)

    def parse_trainer(self, response):
        trainer_data = TrainerResultParser(response.body).parse()
        response.meta['data'] = {**response.meta['data'], **trainer_data}
        yield scrapy.Request(response.urljoin(f"/jockey/result/{response.meta['data']['j_key']}"),
                             callback=self.parse_jockey, meta=response.meta, dont_filter=True)

    def parse_jockey(self, response):
        jockey_data = JockeyResultParser(response.body).parse()
        yield {**response.meta['data'], **jockey_data}
