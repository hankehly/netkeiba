import re
from datetime import datetime

from bs4 import Comment

from netkeiba.parsers.parser import Parser


class HorseParser(Parser):
    def parse(self):
        win_record_str = self.soup.select('.db_prof_table tr')[-3].select_one('td').contents[0]
        win_record_matches = re.search('([0-9]+)戦([0-9]+)勝', win_record_str)
        h_total_races = int(win_record_matches.group(1))
        h_total_wins = int(win_record_matches.group(2))

        birthday_string = self.soup.select_one('.db_prof_table tr:nth-of-type(1) td').string
        h_birthday = datetime.strptime(birthday_string, '%Y年%m月%d日').strftime("%Y-%m-%d")

        h_user_rating = None
        if self.soup.select_one('.horse_title .rate strong'):
            for child in self.soup.select_one('.horse_title .rate strong').children:
                if isinstance(child, Comment):
                    child.extract()
            h_user_rating = float(self.soup.select_one('.horse_title .rate strong').string)

        h_sex = None
        if '牝' in self.soup.select_one('.horse_title .txt_01').string:
            h_sex = 'female'
        elif '牡' in self.soup.select_one('.horse_title .txt_01').string:
            h_sex = 'male'
        elif 'セ' in self.soup.select_one('.horse_title .txt_01').string:
            h_sex = 'castrated'

        return {
            'h_total_races': h_total_races,
            'h_total_wins': h_total_wins,
            'h_birthday': h_birthday,
            'h_sex': h_sex,
            'h_user_rating': h_user_rating
        }
