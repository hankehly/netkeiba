import logging
import re
from datetime import datetime

from constants import RACETRACKS, COURSE_TYPES, WEATHER, IMPOST_CATEGORIES
from crawler.parsers.parser import Parser

logger = logging.getLogger(__name__)


class RaceParser(Parser):
    def parse(self):
        racetrack_name = RACETRACKS.get(self._soup.select_one('.race_place .active').string)
        racetrack_id = self._persistor.get('racetrack', name=racetrack_name).get('id')

        track_details = self._soup.select_one('.mainrace_data p span').string \
            .replace(u'\xa0', u'') \
            .replace(' ', '') \
            .split('/')

        course_type_name = track_details[0][0].get(COURSE_TYPES)
        course_type_id = self._persistor.get('course_type', name=course_type_name).get('id')

        distance = int(re.search('([0-9]+)', track_details[0]).group(1))

        data = {'distance': distance, 'course_type_id': course_type_id, 'racetrack_id': racetrack_id}

        if '芝:良' in track_details[2]:
            data['turf_condition'] = f"'good'"
        elif '芝:稍重' in track_details[2]:
            data['turf_condition'] = f"'slightly_heavy'"
        elif '芝:重' in track_details[2]:
            data['turf_condition'] = f"'heavy'"
        elif '芝:不良' in track_details[2]:
            data['turf_condition'] = f"'bad'"

        if 'ダート:良' in track_details[2]:
            data['dirt_condition'] = f"'good'"
        elif 'ダート:稍重' in track_details[2]:
            data['dirt_condition'] = f"'slightly_heavy'"
        elif 'ダート:重' in track_details[2]:
            data['dirt_condition'] = f"'heavy'"
        elif 'ダート:不良' in track_details[2]:
            data['dirt_condition'] = f"'bad'"

        for key, val in WEATHER.items():
            if key in track_details[1]:
                data['weather'] = f"'{val}'"

        subtitle = self._soup.select_one('.mainrace_data .smalltxt').string \
            .replace(u'\xa0', u' ') \
            .replace('  ', ' ') \
            .split(' ')

        for key, val in IMPOST_CATEGORIES.items():
            if key in subtitle[-1]:
                data['impost_category'] = f"'{val}'"

        data['date'] = datetime.strptime(subtitle[0], '%Y年%m月%d日').strftime("'%Y-%m-%d'")

        data['is_non_winner_regional_horse_allowed'] = 1 if '(指定)' in subtitle[-1] else 0
        data['is_winner_regional_horse_allowed'] = 1 if '特指' in subtitle[-1] else 0
        data['is_regional_jockey_allowed'] = 1 if '[指定]' in subtitle[-1] else 0
        data['is_foreign_horse_allowed'] = 1 if '混' in subtitle[-1] else 0
        data['is_foreign_horse_and_trainer_allowed'] = 1 if '国際' in subtitle[-1] else 0
        data['is_apprentice_jockey_allowed'] = 1 if '見習騎手' in subtitle[-1] else 0
        data['is_female_only'] = 1 if '牝' in subtitle[-1] else 0

        race_id = self._persistor.update_or_create('race', '{TODO: KEY}', **data)

        for i, record in enumerate(self._soup.select('.race_table_01 tr')[1:], start=1):
            # (失) 失格 (http://www.jra.go.jp/judge/)
            # (取) 出走取消 (http://jra.jp/faq/pop02/2_7.html)
            # (除) 競走除外 (http://jra.jp/faq/pop02/2_7.html)
            # (中) 競走中止 (http://jra.jp/faq/pop02/2_8.html)
            order_of_finish = record.select('td')[0].string
            if order_of_finish in ['失', '取', '除', '中']:
                logger.info(f"ignoring race_contender({i}) for reason({order_of_finish})")
                continue

            # N(降) 降着 (http://www.jra.go.jp/judge/)
            order_of_finish_lowered = '降' in order_of_finish

            if order_of_finish_lowered:
                order_of_finish = re.search('[0-9]+', order_of_finish).group(0)

            contender = {'race_id': race_id, 'order_of_finish': int(order_of_finish),
                         'order_of_finish_lowered': order_of_finish_lowered}

            horse_key = re.search('/horse/([0-9]+)', record.select('td')[3].select_one('a').get('href')).group(1)
            contender['horse_id'] = self._persistor.get_or_create('horses', horse_key).get('id')

            jockey_key = re.search('/jockey/([0-9]+)', record.select('td')[6].select_one('a').get('href')).group(1)
            contender['jockey_id'] = self._persistor.get_or_create('jockeys', jockey_key).get('id')

            trainer_key = re.search('/trainer/([0-9]+)', record.select('td')[18].select_one('a').get('href')).group(1)
            contender['trainer_id'] = self._persistor.get_or_create('trainers', trainer_key).get('id')

            contender['post_position'] = int(record.select('td')[1].string)

            contender['weight_carried'] = float(record.select('td')[5].string)

            minutes, seconds = map(float, record.select('td')[7].string.split(':'))
            contender['finish_time'] = minutes * 60 + seconds

            contender['first_place_odds'] = float(record.select('td')[12].string)
            contender['popularity'] = float(record.select('td')[13].string)

            horse_weight_search = re.search('([0-9]+)\(([+-]?[0-9]+)\)', record.select('td')[14].string)
            contender['horse_weight'] = int(horse_weight_search.group(1))
            contender['horse_weight_diff'] = int(horse_weight_search.group(2))

    def save(self):
        pass
