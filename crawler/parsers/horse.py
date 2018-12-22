import re
from datetime import datetime

from bs4 import Comment

from crawler.parsers.parser import Parser


class HorseParser(Parser):
    def parse(self):
        key = self._parse_key()
        total_races = self._parse_total_races()
        total_wins = self._parse_total_wins()
        birthday = self._parse_birthday()
        sex = self._parse_sex()
        user_rating = self._parse_user_rating()

        self.data = {
            'key': key,
            'total_races': total_races,
            'total_wins': total_wins,
            'birthday': birthday,
            'sex': sex,
            'user_rating': user_rating
        }

    def persist(self):
        key = self.data.get('key')
        sex_name = self.data.get('sex')
        sex_id = self._persistor.get('horse_sex', name=sex_name).get('id')
        defaults = {
            'total_races': self.data.get('total_races'),
            'total_wins': self.data.get('total_wins'),
            'birthday': self.data.get('birthday'),
            'user_rating': self.data.get('user_rating'),
            'sex_id': sex_id
        }
        self._persistor.update_or_create('horse', defaults=defaults, key=key)

    def _parse_key(self):
        url = self._soup.head.select_one('link[rel=canonical]').get('href')
        return re.search('/horse/([0-9]+)', url).group(1)

    def _parse_total_races(self):
        win_record_str = self._soup.select('.db_prof_table tr')[-3].select_one('td').contents[0]
        win_record_matches = re.search('([0-9]+)戦([0-9]+)勝', win_record_str)
        return int(win_record_matches.group(1))

    def _parse_total_wins(self):
        win_record_str = self._soup.select('.db_prof_table tr')[-3].select_one('td').contents[0]
        win_record_matches = re.search('([0-9]+)戦([0-9]+)勝', win_record_str)
        return int(win_record_matches.group(2))

    def _parse_birthday(self):
        birthday_string = self._soup.select_one('.db_prof_table tr:nth-of-type(1) td').string
        return datetime.strptime(birthday_string, '%Y年%m月%d日').strftime('%Y-%m-%d')

    def _parse_sex(self):
        sex = None
        if '牝' in self._soup.select_one('.horse_title .txt_01').string:
            sex = 'female'
        elif '牡' in self._soup.select_one('.horse_title .txt_01').string:
            sex = 'male'
        elif 'セ' in self._soup.select_one('.horse_title .txt_01').string:
            sex = 'castrated'
        return sex

    def _parse_user_rating(self):
        user_rating = None
        if self._soup.select_one('.horse_title .rate strong'):
            for child in self._soup.select_one('.horse_title .rate strong').children:
                if isinstance(child, Comment):
                    child.extract()
            user_rating = float(self._soup.select_one('.horse_title .rate strong').string)
        return user_rating
