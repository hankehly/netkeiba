from bs4 import BeautifulSoup

from crawler.persistor import DjangoPersistor

persistor = DjangoPersistor()


class Parser:
    def __init__(self, html):
        self._persistor = persistor
        self._soup = BeautifulSoup(html, 'html.parser')
        self.data = None

    def str2float(self, value: str) -> float:
        return float(value.replace(',', ''))

    def str2int(self, value: str) -> int:
        return int(value.replace(',', ''))

    def parse(self):
        raise NotImplementedError

    def persist(self):
        raise NotImplementedError
