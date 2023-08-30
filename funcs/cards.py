from config import COUNT_SYMBOLS_IN_SERIAL_CARD, COUNT_LITTERS_IN_SERIAL_CARD, COUNT_NUMBERS_IN_SERIAL_CARD
from funcs.check_type import check_int


def split_serial_of_card(serial: str):
    litters = ''
    numeric = ''
    i = 0
    while i < len(serial):
        if check_int(serial[i]):
            numeric += serial[i]
        else:
            litters += serial[i]
        i += 1
    if len(litters) > COUNT_LITTERS_IN_SERIAL_CARD:
        return -1
    if len(litters) + len(numeric) != COUNT_SYMBOLS_IN_SERIAL_CARD:
        return -2

    return [litters, numeric]


def plus_count_cards(count: int, begin: int):
    if count > 2:
        end = begin + count - 1
        return [begin, end]
    else:
        return [begin, begin]


def check_serial_number_of_valid(number):
    if check_int(number):
        number = str(number)
        if len(number) < COUNT_NUMBERS_IN_SERIAL_CARD:
            i = 0
            nulls = ''
            while i < COUNT_NUMBERS_IN_SERIAL_CARD - len(number):
                nulls += '0'
                i += 1
            number = nulls + number
            return number
        else:
            return number
    else:
        ...
