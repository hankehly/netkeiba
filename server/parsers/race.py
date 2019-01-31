import logging
import re
from datetime import datetime, time

import pytz
from bs4 import Comment

from server.models import Race, Horse
from server.parsers.parser import Parser

logger = logging.getLogger(__name__)

RACETRACKS = {
    '札幌': Race.SAPPORO,
    '函館': Race.HAKODATE,
    '福島': Race.FUMA,
    '新潟': Race.NIIGATA,
    '東京': Race.TOKYO,
    '中山': Race.NAKAYAMA,
    '中京': Race.CHUKYO,
    '京都': Race.KYOTO,
    '阪神': Race.HANSHIN,
    '小倉': Race.OGURA
}

WEATHER = {
    '曇': Race.CLOUDY,
    '晴': Race.SUNNY,
    '小雨': Race.LIGHT_RAIN,
    '雨': Race.RAINY,
    '雪': Race.SNOWY
}

IMPOST_CATEGORIES = {
    '馬齢': Race.HORSE_AGE,
    '定量': Race.WEIGHT_SEX,
    '別定': Race.SET_WEIGHT,
    'ハンデ': Race.HANDICAP
}

COURSE_TYPES = {
    '芝': Race.TURF,
    'ダ': Race.DIRT,
    '障': Race.OBSTACLE
}

HORSE_SEX = {
    '牝': Horse.FEMALE,
    '牡': Horse.MALE,
    'セ': Horse.CASTRATED
}

RACE_CLASSES = {}


class RaceParser(Parser):
    def parse(self):
        self.data = {
            'key': self._parse_key(),
            'racetrack': self._parse_racetrack(),
            'impost_category': self._parse_impost_category(),
            'course_type': self._parse_course_type(),
            'distance': self._parse_distance(),
            'number': self._parse_number(),
            'race_class': self._parse_class(),
            'datetime': self._parse_datetime(),
            'weather': self._parse_weather(),

            'turf_condition': self._parse_turf_condition(),
            'dirt_condition': self._parse_dirt_condition(),
            'is_non_winner_regional_horse_allowed': self._parse_is_non_winner_regional_horse_allowed(),
            'is_winner_regional_horse_allowed': self._parse_is_winner_regional_horse_allowed(),
            'is_regional_jockey_allowed': self._parse_is_regional_jockey_allowed(),
            'is_foreign_horse_allowed': self._parse_is_foreign_horse_allowed(),
            'is_foreign_horse_and_trainer_allowed': self._parse_is_foreign_horse_and_trainer_allowed(),
            'is_apprentice_jockey_allowed': self._parse_is_apprentice_jockey_allowed(),
            'is_female_only': self._parse_is_female_only()
        }

        contenders = []
        for i, record in enumerate(self._soup.select('.race_table_01 tr')[1:], start=1):
            # (失) 失格 (http://www.jra.go.jp/judge/)
            # (取) 出走取消 (http://jra.jp/faq/pop02/2_7.html)
            # (除) 競走除外 (http://jra.jp/faq/pop02/2_7.html)
            # (中) 競走中止 (http://jra.jp/faq/pop02/2_8.html)
            order_of_finish = record.select('td')[0].string
            if order_of_finish in ['失', '取', '除', '中']:
                logger.info(f'ignoring race_contender({i}) for reason({order_of_finish})')
                continue

            # 落馬した騎手が再度騎乗してレースを続けること
            did_remount = '再' in order_of_finish

            # N(降) 降着 (http://www.jra.go.jp/judge/)
            order_of_finish_lowered = '降' in order_of_finish

            if order_of_finish_lowered or did_remount:
                order_of_finish = re.search('[0-9]+', order_of_finish).group(0)

            minutes, seconds = map(float, record.select('td')[7].string.split(':'))
            horse_weight_search = re.search('([0-9]+)\(([+-]?[0-9]+)\)', record.select('td')[14].string)
            horse_url = record.select('td')[3].select_one('a').get('href')
            jockey_url = record.select('td')[6].select_one('a').get('href')
            trainer_url = record.select('td')[18].select_one('a').get('href')

            contender = {
                'order_of_finish': int(order_of_finish),
                'order_of_finish_lowered': order_of_finish_lowered,
                'did_remount': did_remount,
                'post_position': int(record.select('td')[1].string),
                'weight_carried': float(record.select('td')[5].string),
                'first_place_odds': float(record.select('td')[12].string),
                'popularity': float(record.select('td')[13].string),
                'horse_key': re.search('/horse/([0-9]+)', horse_url).group(1),
                'jockey_key': re.search('/jockey/([0-9]+)', jockey_url).group(1),
                'trainer_key': re.search('/trainer/([0-9]+)', trainer_url).group(1),
                'finish_time': minutes * 60 + seconds,
            }

            if horse_weight_search:
                contender['horse_weight'] = int(horse_weight_search.group(1))
                contender['horse_weight_diff'] = int(horse_weight_search.group(2))

            contenders.append(contender)

        self.data['contenders'] = contenders

    def persist(self):
        pass
        # TODO: Create missing objects like turf condition category as you see them
        # race_key = self.data.get('key')
        # racetrack_id = RaceTrack.objects.get(name=self.data.get('racetrack')).id
        # course_type_id = CourseType.objects.get(name=self.data.get('course_type')).id
        # turf_condition = self.data.get('turf_condition')
        # dirt_condition = self.data.get('dirt_condition')
        #
        # if turf_condition:
        #     turf_condition_id = TurfConditionCategory.objects.get(name=turf_condition).id
        # else:
        #     turf_condition_id = None
        #
        # if dirt_condition:
        #     dirt_condition_id = DirtConditionCategory.objects.get(name=dirt_condition).id
        # else:
        #     dirt_condition_id = None
        #
        # weather_category_id = WeatherCategory.objects.get(name=self.data.get('weather')).id
        # impost_category_id = ImpostCategory.objects.get(name=self.data.get('impost_category')).id
        # race, _ = Race.objects.update_or_create(key=race_key, defaults={
        #     'racetrack_id': racetrack_id,
        #     'course_type_id': course_type_id,
        #     'turf_condition_id': turf_condition_id,
        #     'dirt_condition_id': dirt_condition_id,
        #     'distance': self.data.get('distance'),
        #     'weather_id': weather_category_id,
        #     'impost_category_id': impost_category_id,
        #     'datetime': self.data.get('datetime')
        # })
        #
        # if self.data.get('is_non_winner_regional_horse_allowed'):
        #     NonWinnerRegionalHorseRace.objects.update_or_create(race=race)
        #
        # if self.data.get('is_winner_regional_horse_allowed'):
        #     WinnerRegionalHorseRace.objects.update_or_create(race=race)
        #
        # if self.data.get('is_regional_jockey_allowed'):
        #     RegionalJockeyRace.objects.update_or_create(race=race)
        #
        # if self.data.get('is_foreign_horse_allowed'):
        #     ForeignHorseRace.objects.update_or_create(race=race)
        #
        # if self.data.get('is_foreign_horse_and_trainer_allowed'):
        #     ForeignTrainerHorseRace.objects.update_or_create(race=race)
        #
        # if self.data.get('is_apprentice_jockey_allowed'):
        #     ApprenticeJockeyRace.objects.update_or_create(race=race)
        #
        # if self.data.get('is_female_only'):
        #     FemaleOnlyRace.objects.update_or_create(race=race)
        #
        # for contender in self.data.get('contenders'):
        #     horse = Horse.objects.get_or_create(key=contender.get('horse_key'))
        #     jockey = Jockey.objects.get_or_create(key=contender.get('jockey_key'))
        #     trainer = Trainer.objects.get_or_create(key=contender.get('trainer_key'))
        #     defaults = {
        #         'order_of_finish': contender.get('order_of_finish'),
        #         'order_of_finish_lowered': contender.get('order_of_finish_lowered'),
        #         'did_remount': contender.get('did_remount'),
        #         'post_position': contender.get('post_position'),
        #         'weight_carried': contender.get('weight_carried'),
        #         'first_place_odds': contender.get('first_place_odds'),
        #         'popularity': contender.get('popularity'),
        #         'finish_time': contender.get('finish_time'),
        #         'horse_weight': contender.get('horse_weight'),
        #         'horse_weight_diff': contender.get('horse_weight_diff'),
        #     }
        #     RaceContender.objects.update_or_create(race=race, horse_id=horse.id, jockey_id=jockey.id,
        #                                            trainer_id=trainer.id, defaults=defaults)

    @property
    def _track_details(self):
        return self._soup.select_one('.mainrace_data p span').string.replace(u'\xa0', u'').replace(' ', '').split('/')

    @property
    def _subtitle(self):
        return self._soup.select_one('.mainrace_data .smalltxt').string.replace(u'\xa0', u' ').replace('  ', ' ') \
            .split(' ')

    def _parse_key(self):
        race_url = self._soup.select_one('.race_num.fc .active').get('href')
        return re.search('/race/([0-9]+)', race_url).group(1)

    def _parse_racetrack(self):
        string = self._subtitle[1]
        match = None
        for key, val in RACETRACKS.items():
            if re.search(key, string):
                match = val
                break
        return match

    def _parse_impost_category(self):
        string = self._subtitle[-1]
        match = None
        for key, val in IMPOST_CATEGORIES.items():
            if key in string:
                match = val
                break
        return match

    def _parse_course_type(self):
        string = self._track_details[0][0]
        return COURSE_TYPES.get(string)

    def _parse_distance(self):
        string = self._track_details[0]
        match = re.search('([0-9]+)m', string).group(1)
        return int(match)

    def _parse_number(self):
        string = self._soup.select_one('.mainrace_data .racedata dt').string.strip()
        return int(string.split(' ')[0])

    def _parse_class(self):
        string = self._soup.select_one('.mainrace_data h1')
        for child in string.children:
            if isinstance(child, Comment):
                child.extract()
        match = None
        for key, val in RACE_CLASSES.items():
            if key in string:
                match = val
                break
        return match

    def _parse_datetime(self):
        race_date = self._parse_date()
        race_time = self._parse_time()
        jst = pytz.timezone('Asia/Tokyo')
        dt = datetime.combine(race_date, race_time)
        return jst.localize(dt)

    def _parse_date(self):
        return datetime.strptime(self._subtitle[0], '%Y年%m月%d日').date()

    def _parse_time(self):
        time_str = re.search('[0-9]{2}:[0-9]{2}', self._track_details[-1]).group()
        hours, minutes = list(map(int, time_str.split(':')))
        return time(hours, minutes)

    def _parse_weather(self):
        string = self._track_details[1]
        match = None
        for key, val in WEATHER.items():
            if key in string:
                match = val
                break
        return match

    def _parse_turf_condition(self):
        turf_condition = None
        if '芝:良' in self._track_details[2]:
            turf_condition = 'good'
        elif '芝:稍重' in self._track_details[2]:
            turf_condition = 'slightly_heavy'
        elif '芝:重' in self._track_details[2]:
            turf_condition = 'heavy'
        elif '芝:不良' in self._track_details[2]:
            turf_condition = 'bad'

        return turf_condition

    def _parse_dirt_condition(self):
        dirt_condition = None
        if 'ダート:良' in self._track_details[2]:
            dirt_condition = 'good'
        elif 'ダート:稍重' in self._track_details[2]:
            dirt_condition = 'slightly_heavy'
        elif 'ダート:重' in self._track_details[2]:
            dirt_condition = 'heavy'
        elif 'ダート:不良' in self._track_details[2]:
            dirt_condition = 'bad'

        return dirt_condition

    def _parse_is_non_winner_regional_horse_allowed(self):
        return '(指定)' in self._subtitle[-1]

    def _parse_is_winner_regional_horse_allowed(self):
        return '特指' in self._subtitle[-1]

    def _parse_is_regional_jockey_allowed(self):
        return '[指定]' in self._subtitle[-1]

    def _parse_is_foreign_horse_allowed(self):
        return '混' in self._subtitle[-1]

    def _parse_is_foreign_horse_and_trainer_allowed(self):
        return '国際' in self._subtitle[-1]

    def _parse_is_apprentice_jockey_allowed(self):
        return '見習騎手' in self._subtitle[-1]

    def _parse_is_female_only(self):
        return '牝' in self._subtitle[-1]
