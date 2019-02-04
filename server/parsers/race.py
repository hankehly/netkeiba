import logging
import re
from datetime import datetime, time, timedelta
from typing import Optional

import pytz
from bs4 import Comment

from server.models import Race, Horse, RaceContender, Trainer
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
    '定量': Race.WEIGHT_FOR_AGE,
    '別定': Race.SET_WEIGHT,
    'ハンデ': Race.HANDICAP
}

SURFACES = {
    '芝': Race.TURF,
    'ダ': Race.DIRT,
}

COURSE_TYPES = {
    '左': Race.LEFT,
    '右': Race.RIGHT,
    '直線': Race.STRAIGHT,
    '障': Race.OBSTACLE
}

HORSE_SEX = {
    '牝': Horse.FEMALE,
    '牡': Horse.MALE,
    'セ': Horse.CASTRATED
}

RACE_CLASSES = {
    'オープン': Race.OPEN,
    '1600万下': Race.U1600,
    '1000万下': Race.U1000,
    '500万下': Race.U500,
    '未勝利': Race.MAIDEN,
    '新馬': Race.UNRACED_MAIDEN,
}

POSITION_STATES = {
    '失': RaceContender.DISQUALIFIED,
    '取': RaceContender.CANCELLED,
    '除': RaceContender.CANCELLED,
    '再': RaceContender.REMOUNT,
    '中': RaceContender.NO_FINISH,
    '降': RaceContender.POSITION_LOWERED,
}

STABLES = {
    '東': Trainer.EAST,
    '西': Trainer.WEST,
    '地': Trainer.REGIONAL,
    '外': Trainer.OVERSEAS,
}

MARGINS = {
    'ハナ': RaceContender.NOSE,
    'クビ': RaceContender.NECK,
    'アタマ': RaceContender.HEAD,
}


class RaceParser(Parser):
    def parse(self):
        self.data = {
            'key': self._parse_key(),
            'racetrack': self._parse_racetrack(),
            'impost_category': self._parse_impost_category(),
            'surface': self._parse_surface(),
            'course': self._parse_course(),
            'distance': self._parse_distance(),
            'number': self._parse_number(),
            'race_class': self._parse_class(),
            'grade': self._parse_grade(),
            'datetime': self._parse_datetime(),
            'weather': self._parse_weather(),
            'track_condition': self._parse_track_condition(),
            'is_outside_racetrack': self._parse_is_outside_racetrack(),
            'is_regional_maiden_race': self._parse_is_regional_maiden_race(),
            'is_winner_regional_horse_race': self._parse_is_winner_regional_horse_race(),
            'is_regional_jockey_race': self._parse_is_regional_jockey_race(),
            'is_foreign_horse_race': self._parse_is_foreign_horse_race(),
            'is_foreign_trainer_horse_race': self._parse_is_foreign_trainer_horse_race(),
            'is_apprentice_jockey_race': self._parse_is_apprentice_jockey_race(),
            'is_female_only_race': self._parse_is_female_only_race()
        }

        contenders = []
        for i, record in enumerate(self._contender_rows, start=1):
            contenders.append({
                'horse': self._parse_contender_horse(i),
                'jockey': self._parse_contender_jockey(i),
                'trainer': self._parse_contender_trainer(i),
                'trainer__stable': self._parse_contender_trainer_stable(i),
                'owner': self._parse_contender_owner(i),
                'order_of_finish': self._parse_contender_order_of_finish(i),
                'position_state': self._parse_contender_position_state(i),
                'post_position': self._parse_contender_post_position(i),
                'horse_number': self._parse_contender_horse_number(i),
                'weight_carried': self._parse_contender_weight_carried(i),
                'finish_time': self._parse_contender_finish_time(i),
                'margin': self._parse_contender_margin(i),
                'final_stage_time': self._parse_contender_final_stage_time(i),
                'first_place_odds': self._parse_contender_first_place_odds(i),
                'popularity': self._parse_contender_popularity(i),
                'horse_weight': self._parse_contender_horse_weight(i),
                'horse_weight_diff': self._parse_contender_horse_weight_diff(i),
                'purse': self._parse_contender_purse(i),
            })
        self.data['contenders'] = contenders

    def persist(self):
        pass
        # TODO: Create missing objects like turf condition category as you see them
        # TODO: horse_number
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
        return self._soup.select_one('.mainrace_data p span').string \
            .replace(u'\xa0', u'') \
            .replace(' ', '') \
            .split('/')

    @property
    def _subtitle(self):
        return self._soup.select_one('.mainrace_data .smalltxt').string \
            .replace(u'\xa0', u' ') \
            .replace('  ', ' ') \
            .split(' ')

    @property
    def _contender_rows(self):
        return self._soup.select('.race_table_01 tr')[1:]

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

    def _parse_surface(self):
        string = self._track_details[0][0]
        return SURFACES.get(string)

    def _parse_course(self):
        string = self._track_details[0][0]
        return COURSE_TYPES.get(string)

    def _parse_is_outside_racetrack(self):
        return '外' in self._track_details[0][0]

    def _parse_distance(self):
        string = self._track_details[0]
        match = re.search('([0-9]+)m', string).group(1)
        return int(match)

    def _parse_number(self):
        string = self._soup.select_one('.mainrace_data .racedata dt').string.strip()
        return int(string.split(' ')[0])

    def _parse_class(self):
        string = self._subtitle[-2]
        match = None
        for key, val in RACE_CLASSES.items():
            if key in string:
                match = val
                break
        return match

    def _parse_grade(self):
        string = self._soup.select_one('.mainrace_data h1')
        for child in string.children:
            if isinstance(child, Comment):
                child.extract()
        match = Race.NOT_APPLICABLE
        for grade in [Race.G1, Race.G2, Race.G3]:
            if grade in string:
                match = grade
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

    def _parse_track_condition(self):
        string = self._track_details[2]
        match = None
        if '不良' in string:
            match = Race.BAD
        elif '良' in string:
            match = Race.GOOD
        elif '稍重' in string:
            match = Race.SLIGHTLY_HEAVY
        elif '重' in string:
            match = Race.HEAVY
        return match

    def _parse_is_regional_maiden_race(self):
        return '(指定)' in self._subtitle[-1]

    def _parse_is_winner_regional_horse_race(self):
        return '特指' in self._subtitle[-1]

    def _parse_is_regional_jockey_race(self):
        return '[指定]' in self._subtitle[-1]

    def _parse_is_foreign_horse_race(self):
        return '混' in self._subtitle[-1]

    def _parse_is_foreign_trainer_horse_race(self):
        return '国際' in self._subtitle[-1]

    def _parse_is_apprentice_jockey_race(self):
        return '見習騎手' in self._subtitle[-1]

    def _parse_is_female_only_race(self):
        return '牝' in self._subtitle[-1]

    def _parse_contender_horse(self, i):
        horse_url = self._contender_rows[i].select('td')[3].select_one('a').get('href')
        return re.search('/horse/([0-9]+)', horse_url).group(1)

    def _parse_contender_jockey(self, i):
        jockey_url = self._contender_rows[i].select('td')[6].select_one('a').get('href')
        return re.search('/jockey/([0-9]+)', jockey_url).group(1)

    def _parse_contender_trainer(self, i):
        trainer_url = self._contender_rows[i].select('td')[18].select_one('a').get('href')
        return re.search('/trainer/([0-9]+)', trainer_url).group(1)

    def _parse_contender_trainer_stable(self, i):
        string = self._contender_rows[i].select('td')[18].text
        stable_char = re.search('\[(東|西|地|外)\]', string).group(1)
        match = None
        for key, value in STABLES.items():
            if stable_char == key:
                match = key
                break
        return match

    def _parse_contender_owner(self, i):
        owner_url = self._contender_rows[i].select('td')[19].select_one('a').get('href')
        return re.search('/owner/([0-9]+)', owner_url).group(1)

    def _parse_contender_order_of_finish(self, i):
        string = self._contender_rows[i].select('td')[0].string
        match = re.search('[0-9]+', string)
        return match.group() if match else None

    def _parse_contender_position_state(self, i):
        string = self._contender_rows[i].select('td')[0].string
        match = RaceContender.OK
        for key, value in POSITION_STATES.items():
            if key in string:
                match = value
                break
        return match

    def _parse_contender_post_position(self, i):
        string = self._contender_rows[i].select('td')[1].string
        return int(string)

    def _parse_contender_weight_carried(self, i):
        string = self._contender_rows[i].select('td')[5].string
        return float(string)

    def _parse_contender_horse_number(self, i):
        string = self._contender_rows[i].select('td')[2].string
        return int(string)

    def _parse_contender_finish_time(self, i) -> float:
        string = self._contender_rows[i].select('td')[7].string
        dt = datetime.strptime(string, '%M:%S.%f')
        td = timedelta(minutes=dt.minute, seconds=dt.second, microseconds=dt.microsecond)
        return td.total_seconds()

    def _parse_contender_margin(self, i):
        string = self._contender_rows[i].select('td')[8].string
        match = None
        if re.search('[0-9]', string) is None:
            for key, value in MARGINS.items():
                if string == key:
                    match = value
                    break
        else:
            match = RaceContender.OTHER
        return match

    def _parse_contender_final_stage_time(self, i):
        string = self._contender_rows[i].select('td')[11].string
        return float(string)

    def _parse_contender_first_place_odds(self, i):
        string = self._contender_rows[i].select('td')[12].string
        return float(string)

    def _parse_contender_popularity(self, i):
        string = self._contender_rows[i].select('td')[13].string
        return int(string)

    def _parse_contender_horse_weight(self, i) -> Optional[int]:
        string = self._contender_rows[i].select('td')[14].string
        match = re.search('([0-9]+)\(([+-]?[0-9]+)\)', string)
        return int(match.group(1)) if match else None

    def _parse_contender_horse_weight_diff(self, i) -> Optional[int]:
        string = self._contender_rows[i].select('td')[14].string
        match = re.search('([0-9]+)\(([+-]?[0-9]+)\)', string)
        return int(match.group(2)) if match else None

    def _parse_contender_purse(self, i):
        string = self._contender_rows[i].select('td')[-1].string.replace(',', '')
        return float(string)
