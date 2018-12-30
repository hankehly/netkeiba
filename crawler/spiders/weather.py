import scrapy

from server.models import Race


class WeatherSpider(scrapy.Spider):
    """
    https://www.data.jma.go.jp/obd/stats/etrn/view/10min_a1.php?prec_no=45&block_no=1236&year=2018&month=12&day=2
    """
    name = 'weather'
    allowed_domains = ['www.data.jma.go.jp']

    def start_requests(self):
        urls = []
        base_url = 'https://www.data.jma.go.jp/obd/stats/etrn/view/10min_a1.php?prec_no=45&'
        for race in Race.objects.all():
            block_no = self._get_racetrack_block_no(race.racetrack.name)
            year = race.date.year
            month = race.date.month
            day = race.date.day
            url = f'{base_url}block_no={block_no}&year={year}&month={month}&day={day}'
            urls.append(url)
        return urls

    def parse(self, response):
        pass

    def _get_racetrack_block_no(self, name: str) -> str:
        """
        TODO: Implement
        """
        return '1236'
