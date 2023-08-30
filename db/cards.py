from . import query

class Diller:
    def __init__(self, diller: str = None, cards_begin: str = None, cards_end: str = None,
                 search_serial: str = None):
        self.diller = diller
        self.serial_search = search_serial
        self.cards_begin = cards_begin
        self.cards_end = cards_end


class Billing:
    def get_summa(self, serial: str):
        ...
