from . import query
from funcs import dt


def new(type_rec: int, summa: float, desc: str) -> bool:
    try:
        sql = 'insert into bot_finance (type, summa, dsc) values (%s, %s, %s)'
        return query(sql, type_rec, summa, desc, commit=True)
    except Exception as e:
        print(f'FINANCES.NEW (ERROR): {e}')
        return False


def show(all_: bool = False, begin_date: str = '0000-00-00', end_date: str = '0000-00-00') -> list[tuple] | int | None:
    try:
        if all_ is False:
            sql = 'select * from bot_finance where date_add>%s and date_add<%s'
            res = query(sql, begin_date, end_date)
            if res is not False and res is not None and len(res) > 0:
                return res
            else:
                return None
        else:
            sql = 'select * from bot_finance'
            res = query(sql)
            if res is not False and res is not None and len(res) > 0:
                return res
            else:
                return None
    except Exception as e:
        print(f'FINANCE.SHOW (ERROR): {e}')
        return -1
