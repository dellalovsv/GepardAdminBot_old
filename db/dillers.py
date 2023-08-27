from . import query
from funcs import dt


def check_diller(diller: str | int) -> bool:
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
