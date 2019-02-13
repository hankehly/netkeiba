from netkeiba.parsers.parser import Parser


class NoopParser(Parser):
    def parse(self):
        self.data = {}

    def persist(self):
        pass
