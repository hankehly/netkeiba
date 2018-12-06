import re
from datetime import datetime

import scrapy
from bs4 import BeautifulSoup

from netkeiba.parsers.horse import HorseParser
from netkeiba.parsers.jockey import JockeyParser
from netkeiba.parsers.trainer import TrainerParser

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


# 'c_id', (not needed)
# 'c_weight_carried',
# 'c_post_position', (day of)
# 'c_order_of_finish',
# 'c_order_of_finish_lowered',
# 'c_finish_time',
# 'c_horse_weight',
# 'c_horse_weight_diff', (day of)
# 'c_popularity',
# 'c_first_place_odds',
# 'r_id',
# 'r_key',
# 'r_racetrack',
# 'r_course_type',
# 'r_weather',
# 'r_url',
# 'r_distance',
# 'r_date',
# 'r_dirt_condition', (day of)
# 'r_turf_condition', (day of)
# 'r_impost_category',
# 'r_is_non_winner_regional_horse_allowed',
# 'r_is_winner_regional_horse_allowed',
# 'r_is_regional_jockey_allowed',
# 'r_is_foreign_horse_allowed',
# 'r_is_foreign_horse_and_trainer_allowed',
# 'r_is_apprentice_jockey_allowed',
# 'r_is_female_only',
# 'h_id',
# 'h_key',
# 'h_url',
# 'h_total_races',
# 'h_total_wins',
# 'h_sex',
# 'h_birthday',
# 'h_user_rating',
# 'j_id',
# 'j_key',
# 'j_url',
# 'j_career_1st_place_count',
# 'j_career_2nd_place_count',
# 'j_career_3rd_place_count',
# 'j_career_4th_place_or_below_count',
# 'j_career_turf_race_count',
# 'j_career_turf_win_count',
# 'j_career_dirt_race_count',
# 'j_career_dirt_win_count',
# 'j_career_1st_place_rate',
# 'j_career_1st_2nd_place_rate',
# 'j_career_any_place_rate',
# 'j_career_earnings',
# 't_id',
# 't_key',
# 't_url',
# 't_career_1st_place_count',
# 't_career_2nd_place_count',
# 't_career_3rd_place_count',
# 't_career_4th_place_or_below_count',
# 't_career_turf_race_count',
# 't_career_turf_win_count',
# 't_career_dirt_race_count',
# 't_career_dirt_win_count',
# 't_career_1st_place_rate',
# 't_career_1st_2nd_place_rate',
# 't_career_any_place_rate',
# 't_career_earnings',


class RaceSpider(scrapy.Spider):
    name = 'race'
    allowed_domains = ['race.netkeiba.com']

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        contenders = soup.select_one('.race_table_old').select('tr.bml1')
        contender_count = len(contenders)

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
        r_is_winner_regional_horse_allowed = 1 if '(特指)' in race_category_data else 0
        r_is_regional_jockey_allowed = 1 if '[指定]' in race_category_data else 0
        r_is_foreign_horse_allowed = 1 if '混' in race_category_data else 0
        r_is_foreign_horse_and_trainer_allowed = 1 if '国際' in race_category_data else 0
        r_is_apprentice_jockey_allowed = 1 if '見習騎手' in race_category_data else 0
        r_is_female_only = 1 if '牝' in race_category_data else 0

        for row in contenders:
            h_url = row.select('td')[1].select_one('a').get('href')
            h_key = re.search('/horse/([0-9]+)', h_url).group(1)
            horse_sex_symbol = re.search('[^0-9]', row.select('td')[2].text).group()
            h_sex = HORSE_SEX.get(horse_sex_symbol)
            c_weight_carried = float(row.select('td')[3].text)

            with row.select('td')[4] as jockey_column:
                if jockey_column.select_one("a['href']"):
                    j_url = jockey_column.select_one('a').get('href')
                    j_key = re.search('/jockey/([0-9]+)', j_url).group(1)
                else:
                    j_url = ''
                    j_key = ''

            t_url = row.select('td')[5].select_one('a').get('href')
            t_key = re.search('/trainer/([0-9]+)', t_url).group(1)
            c_first_place_odds = float(row.select('td')[6].text)
            c_popularity = int(row.select('td')[7].text)

            yield scrapy.Request(h_url, callback=self.parse_horse, meta={
                'race': {

                }
            })

    def parse_horse(self, response):
        horse_data = HorseParser(response.body).parse()

    def parse_jockey(self, response):
        jockey_data = JockeyParser(response.body).parse()

    def parse_trainer(self, response):
        trainer_data = TrainerParser(response.body).parse()
