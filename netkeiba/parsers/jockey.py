from netkeiba.parsers.parser import Parser


class JockeyParser(Parser):
    def parse(self):
        row = self.soup.select_one('.race_table_01 tr:nth-of-type(3)')

        return {
            'j_career_1st_place_count': self.str2int(row.select_one('td:nth-of-type(3) a').string),
            'j_career_2nd_place_count': self.str2int(row.select_one('td:nth-of-type(4) a').string),
            'j_career_3rd_place_count': self.str2int(row.select_one('td:nth-of-type(5) a').string),
            'j_career_4th_place_or_below_count': self.str2int(row.select_one('td:nth-of-type(6) a').string),
            'j_career_turf_race_count': self.str2int(row.select_one('td:nth-of-type(13) a').string),
            'j_career_turf_win_count': self.str2int(row.select_one('td:nth-of-type(14) a').string),
            'j_career_dirt_race_count': self.str2int(row.select_one('td:nth-of-type(15) a').string),
            'j_career_dirt_win_count': self.str2int(row.select_one('td:nth-of-type(16) a').string),
            'j_career_1st_place_rate': self.str2float(row.select_one('td:nth-of-type(17)').string),
            'j_career_1st_2nd_place_rate': self.str2float(row.select_one('td:nth-of-type(18)').string),
            'j_career_any_place_rate': self.str2float(row.select_one('td:nth-of-type(19)').string),
            'j_career_earnings': self.str2float(row.select_one('td:nth-of-type(20)').string),
        }
