from . import query, subscribers
from config import COUNT_SYMBOLS_OF_SERIAL_CARD, COUNT_LITTERS_OF_SERIAL_CARD, COUNT_NUMBERS_OF_SERIAL_CARD


class Billing:
    def __init__(self, serial: str):
        self.serial = serial

    def check_serial(self) -> list | int:
        """
        Проверка валидности серии карты
        :return: list[БУКВЫ, ЦИФРЫ]; int: -1: Error; 100: Много или мало букв в серии; 101: Слишком большое кол-во символов в серии
        """
        try:
            ser_lit: str = ''
            ser_num: str = ''
            i = 0
            while i < len(self.serial):
                try:
                    int(self.serial[i])
                    ser_num += self.serial[i]
                except ValueError:
                    ser_lit += self.serial[i].upper()
                i += 1
            if len(ser_lit) > COUNT_LITTERS_OF_SERIAL_CARD or len(ser_lit) < COUNT_LITTERS_OF_SERIAL_CARD:
                # Кол-во букв в серии не соответствует
                return 100
            if len(ser_num) > COUNT_NUMBERS_OF_SERIAL_CARD:
                ser_num = ser_num[-COUNT_NUMBERS_OF_SERIAL_CARD:]
            if len(ser_num) < COUNT_NUMBERS_OF_SERIAL_CARD:
                while len(ser_num) < COUNT_NUMBERS_OF_SERIAL_CARD:
                    ser_num = '0' + ser_num
            if len(ser_lit) + len(ser_num) == COUNT_SYMBOLS_OF_SERIAL_CARD:
                return [ser_lit, ser_num]
            else:
                return 101
        except Exception as e:
            print(f'CHECK_SERIAL (ERROR): {e}')
            return -1

    def check_status_card(self):
        card = self.check_serial()
        if card != -1 and card != 100 and card != 101:
            sql = 'select status from cards_users where serial=%s and number=%s'
            res = query(sql, card[0], card[1])
            if res is not False and res is not None and len(res) > 0:
                if res[0]['status'] == 0:
                    return True
                else:
                    return False
            else:
                return None
        else:
            return -1
