import re
from datetime import datetime

import scrapy
from bs4 import BeautifulSoup

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


class RaceSpider(scrapy.Spider):
    name = 'race'
    allowed_domains = ['race.netkeiba.com']

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        contenders = soup.select_one('.race_table_old').select('tr.bml1')
        contender_count = len(contenders)

        r_racetrack = RACETRACKS.get(soup.select_one('.race_place a.active').text)
        r_date = datetime.strptime(re.search('[0-9]{4}/[0-9]{2}/[0-9]{2}', soup.title.text).group(), '%Y/%m/%d').date()
        r_distance = int(re.search('([0-9]+)m', soup.select_one('.racedata').select('p')[0].text).group(1))

        for row in contenders:
            horse_url = row.select('td')[1].select_one('a').get('href')
            horse_key = re.search('/horse/([0-9]+)', horse_url).group(1)
            horse_sex_symbol = re.search('[^0-9]', row.select('td')[2].text).group()
            horse_sex = {'牝': 'female', '牡': 'male', 'セ': 'castrated'}.get(horse_sex_symbol)
            c_weight_carried = float(row.select('td')[3].text)
            jockey_url = row.select('td')[4].select_one('a').get('href')
            jockey_key = re.search('/jockey/([0-9]+)', jockey_url).group(1)
            trainer_url = row.select('td')[5].select_one('a').get('href')
            trainer_key = re.search('/trainer/([0-9]+)', trainer_url).group(1)
            c_first_place_odds = float(row.select('td')[6].text)
            c_popularity = int(row.select('td')[7].text)
            yield scrapy.Request(horse_url, callback=self.parse_horse)

    def parse_horse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        win_record_str = soup.select('.db_prof_table tr')[-3].select_one('td').contents[0]
        win_record_matches = re.search('([0-9]+)戦([0-9]+)勝', win_record_str)
        total_races = int(win_record_matches.group(1))
        total_wins = int(win_record_matches.group(2))

    def parse_jockey(self, response):
        pass

    def parse_trainer(self, response):
        pass
