from bs4 import BeautifulSoup


class Parser:
    def __init__(self, html):
        self._soup = BeautifulSoup(html, 'html.parser')
        self.data = None

    def parse(self):
        raise NotImplementedError

    def persist(self):
        raise NotImplementedError
