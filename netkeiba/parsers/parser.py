from bs4 import BeautifulSoup


class Parser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def str2float(self, value: str) -> float:
        return float(value.replace(',', ''))

    def str2int(self, value: str) -> int:
        return int(value.replace(',', ''))

    def parse(self):
        raise NotImplementedError
