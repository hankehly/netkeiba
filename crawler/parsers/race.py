import logging
import re
from datetime import datetime

from crawler.constants import RACETRACKS, COURSE_TYPES, WEATHER, IMPOST_CATEGORIES
from crawler.parsers.parser import Parser

logger = logging.getLogger(__name__)


class RaceParser(Parser):
    def parse(self):
        distance = self._parse_distance()
        course_type_id = self._parse_course_type_id()
        racetrack_id = self._parse_racetrack_id()

        data = {'distance': distance, 'course_type_id': course_type_id, 'racetrack_id': racetrack_id}

        data['turf_condition'] = self._parse_turf_condition()
        data['dirt_condition'] = self._parse_dirt_condition()
        data['weather'] = self._parse_weather()
        data['impost_category'] = self._parse_impost_category()
        data['date'] = self._parse_date()

        data['is_non_winner_regional_horse_allowed'] = self._parse_is_non_winner_regional_horse_allowed()
        data['is_winner_regional_horse_allowed'] = self._parse_is_winner_regional_horse_allowed()
        data['is_regional_jockey_allowed'] = self._parse_is_regional_jockey_allowed()
        data['is_foreign_horse_allowed'] = self._parse_is_foreign_horse_allowed()
        data['is_foreign_horse_and_trainer_allowed'] = self._parse_is_foreign_horse_and_trainer_allowed()
        data['is_apprentice_jockey_allowed'] = self._parse_is_apprentice_jockey_allowed()
        data['is_female_only'] = self._parse_is_female_only()

        race_key = self._parse_race_key()
        race = self._persistor.update_or_create('race', race_key, **data)

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

            contender = {'race_id': race.get('id'), 'order_of_finish': int(order_of_finish),
                         'order_of_finish_lowered': order_of_finish_lowered}

            horse_key = re.search('/horse/([0-9]+)', record.select('td')[3].select_one('a').get('href')).group(1)
            contender['horse_id'] = self._persistor.get_or_create('horse', horse_key).get('id')

            jockey_key = re.search('/jockey/([0-9]+)', record.select('td')[6].select_one('a').get('href')).group(1)
            contender['jockey_id'] = self._persistor.get_or_create('jockey', jockey_key).get('id')

            trainer_key = re.search('/trainer/([0-9]+)', record.select('td')[18].select_one('a').get('href')).group(1)
            contender['trainer_id'] = self._persistor.get_or_create('trainer', trainer_key).get('id')

            contender['post_position'] = int(record.select('td')[1].string)

            contender['weight_carried'] = float(record.select('td')[5].string)

            minutes, seconds = map(float, record.select('td')[7].string.split(':'))
            contender['finish_time'] = minutes * 60 + seconds

            contender['first_place_odds'] = float(record.select('td')[12].string)
            contender['popularity'] = float(record.select('td')[13].string)

            horse_weight_search = re.search('([0-9]+)\(([+-]?[0-9]+)\)', record.select('td')[14].string)
            contender['horse_weight'] = int(horse_weight_search.group(1))
            contender['horse_weight_diff'] = int(horse_weight_search.group(2))

    def _parse_distance(self):
        track_details = self._soup.select_one('.mainrace_data p span').string \
            .replace(u'\xa0', u'') \
            .replace(' ', '') \
            .split('/')

        return int(re.search('([0-9]+)', track_details[0]).group(1))

    def persist(self):
        pass

    def _parse_course_type_id(self):
        track_details = self._soup.select_one('.mainrace_data p span').string \
            .replace(u'\xa0', u'') \
            .replace(' ', '') \
            .split('/')

        course_type_name = track_details[0][0].get(COURSE_TYPES)
        return self._persistor.get('course_type', name=course_type_name).get('id')

    def _parse_racetrack_id(self):
        racetrack_name = RACETRACKS.get(self._soup.select_one('.race_place .active').string)
        return self._persistor.get('racetrack', name=racetrack_name).get('id')

    def _parse_turf_condition(self):
        track_details = self._soup.select_one('.mainrace_data p span').string \
            .replace(u'\xa0', u'') \
            .replace(' ', '') \
            .split('/')

        turf_condition = None
        if '芝:良' in track_details[2]:
            turf_condition = 'good'
        elif '芝:稍重' in track_details[2]:
            turf_condition = 'slightly_heavy'
        elif '芝:重' in track_details[2]:
            turf_condition = 'heavy'
        elif '芝:不良' in track_details[2]:
            turf_condition = 'bad'

        return turf_condition

    def _parse_dirt_condition(self):
        track_details = self._soup.select_one('.mainrace_data p span').string \
            .replace(u'\xa0', u'') \
            .replace(' ', '') \
            .split('/')

        dirt_condition = None
        if 'ダート:良' in track_details[2]:
            dirt_condition = 'good'
        elif 'ダート:稍重' in track_details[2]:
            dirt_condition = 'slightly_heavy'
        elif 'ダート:重' in track_details[2]:
            dirt_condition = 'heavy'
        elif 'ダート:不良' in track_details[2]:
            dirt_condition = 'bad'

        return dirt_condition

    def _parse_weather(self):
        track_details = self._soup.select_one('.mainrace_data p span').string \
            .replace(u'\xa0', u'') \
            .replace(' ', '') \
            .split('/')

        weather = None
        for key, val in WEATHER.items():
            if key in track_details[1]:
                weather = val

        return weather

    def _parse_impost_category(self):
        subtitle = self._soup.select_one('.mainrace_data .smalltxt').string \
            .replace(u'\xa0', u' ') \
            .replace('  ', ' ') \
            .split(' ')

        impost_category = None
        for key, val in IMPOST_CATEGORIES.items():
            if key in subtitle[-1]:
                impost_category = val

        return impost_category

    def _parse_date(self):
        subtitle = self._soup.select_one('.mainrace_data .smalltxt').string \
            .replace(u'\xa0', u' ') \
            .replace('  ', ' ') \
            .split(' ')

        return datetime.strptime(subtitle[0], '%Y年%m月%d日').strftime("%Y-%m-%d")

    def _parse_race_key(self):
        race_url = self._soup.select_one('.race_place .active').get('href')
        return re.search('/race/([0-9]+)', race_url).group(1)

    def _parse_is_non_winner_regional_horse_allowed(self):
        subtitle = self._soup.select_one('.mainrace_data .smalltxt').string \
            .replace(u'\xa0', u' ') \
            .replace('  ', ' ') \
            .split(' ')

        return '(指定)' in subtitle[-1]

    def _parse_is_winner_regional_horse_allowed(self):
        subtitle = self._soup.select_one('.mainrace_data .smalltxt').string \
            .replace(u'\xa0', u' ') \
            .replace('  ', ' ') \
            .split(' ')

        return '特指' in subtitle[-1]

    def _parse_is_regional_jockey_allowed(self):
        subtitle = self._soup.select_one('.mainrace_data .smalltxt').string \
            .replace(u'\xa0', u' ') \
            .replace('  ', ' ') \
            .split(' ')

        return '[指定]' in subtitle[-1]

    def _parse_is_foreign_horse_allowed(self):
        subtitle = self._soup.select_one('.mainrace_data .smalltxt').string \
            .replace(u'\xa0', u' ') \
            .replace('  ', ' ') \
            .split(' ')

        return '混' in subtitle[-1]

    def _parse_is_foreign_horse_and_trainer_allowed(self):
        subtitle = self._soup.select_one('.mainrace_data .smalltxt').string \
            .replace(u'\xa0', u' ') \
            .replace('  ', ' ') \
            .split(' ')

        return '国際' in subtitle[-1]

    def _parse_is_apprentice_jockey_allowed(self):
        subtitle = self._soup.select_one('.mainrace_data .smalltxt').string \
            .replace(u'\xa0', u' ') \
            .replace('  ', ' ') \
            .split(' ')

        return '見習騎手' in subtitle[-1]

    def _parse_is_female_only(self):
        subtitle = self._soup.select_one('.mainrace_data .smalltxt').string \
            .replace(u'\xa0', u' ') \
            .replace('  ', ' ') \
            .split(' ')

        return '牝' in subtitle[-1]
