import re
from datetime import datetime

from bs4 import Comment

from crawler.parsers.parser import Parser


class HorseParser(Parser):
    def parse(self):
        total_races = self._parse_total_races()
        total_wins = self._parse_total_wins()
        birthday = self._parse_birthday()
        sex = self._parse_sex()
        user_rating = self._parse_user_rating()

        self.data = {
            'total_races': total_races,
            'total_wins': total_wins,
            'birthday': birthday,
            'sex': sex,
            'user_rating': user_rating
        }

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
        return datetime.strptime(birthday_string, '%Y年%m月%d日').strftime("%Y-%m-%d")

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

    def persist(self):
        pass
