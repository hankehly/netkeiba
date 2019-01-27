from bs4 import BeautifulSoup


class Parser:
    def __init__(self, html):
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
