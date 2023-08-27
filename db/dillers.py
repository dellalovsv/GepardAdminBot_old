from . import query
from funcs import dt


def check_exists_diller(diller: str | int) -> bool:
    try:
        sql = 'select id from bot_dillers where id=%s or name=%s'
        res = query(sql, diller, diller)
        if res is not False and res is not None and len(res) > 0:
            return True
        else:
            return False
    except Exception as e:
        print(f'DILLERS.CHECK_DILLER (ERROR): {e}')
        return False


def new_diller(name: str, address: str, phone: str) -> bool | int:
    try:
        if check_exists_diller(name) is False:
            sql = 'insert into bot_dillers (name, address, phone) values (%s, %s, %s)'
            if query(sql, name, address, phone, commit=True):
                return True
            else:
                return False
        else:
            return 1
    except Exception as e:
        print(f'DILLERS.NEW_DILLER (ERROR): {e}')
        return -1


def show(name: str = None):
    try:
        if name is None:
            sql = 'select * from bot_dillers'
            res = query(sql)
        else:
            sql = 'select * from bot_dillers where id=%s or name=%s'
            res = query(sql, name, name)
        if res is not False and res is not None and len(res) > 0:
            return res
        else:
            return None
    except Exception as e:
        print(f'DILLERS.SHOW (ERROR): {e}')
        return -1
