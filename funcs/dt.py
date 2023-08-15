import datetime
from datetime import datetime as dt
from datetime import timedelta as td


def get_date(time: bool = False) -> str:
    if time:
        return dt.now().strftime('%d.%m.%Y %H:%M:%S')
    else:
        return dt.now().strftime('%d.%m.%Y')


def check_begin_date(date: str) -> bool:
    d = conv_date(date)
    d = dt.strptime(d, '%Y-%m-%d')
    if d > dt.now():
        return False
    else:
        return True


def conv_date(date: str = '0000-00-00') -> str | bool:
    try:
        if ":" in date:
            if '-' in date:
                d = dt.strptime(date, "%Y-%m-%d %H:%M:%S")
                return d.strftime("%d.%m.%Y %H:%M:%S")
            elif '.' in date:
                d = dt.strptime(date, "%d.%m.%Y %H:%M:%S")
                return d.strftime("%Y-%m-%d %H:%M:%S")
        elif ":" not in date:
            if '-' in date:
                d = dt.strptime(date, "%Y-%m-%d")
                return d.strftime("%d.%m.%Y")
            elif '.' in date:
                d = dt.strptime(date, "%d.%m.%Y")
                return d.strftime('%Y-%m-%d')
    except Exception as e:
        print(f'DT.CONV_DATE (ERROR): {e}')
        return False


def plus_days(days: int = 0, date: str = '0000-00-00') -> str:
    if date == '0000-00-00':
        d = dt.now()
    else:
        d = dt.strptime(date, "%Y-%m-%d")
    res = d + td(days=days)
    return res.strftime('%Y-%m-%d')


def minus_days(days: int = 0, date: str = '0000-00-00') -> str:
    if date == '0000-00-00':
        d = dt.now()
    else:
        d = dt.strptime(date, "%Y-%m-%d")
    res = d - td(days=days)
    return res.strftime('%Y-%m-%d')


def get_date_of_current_week():
    d = dt.now()
    monday = d - td(days=d.weekday())
    return [monday + td(days=day) for day in range(7)]


def get_first_and_last_date_of_current_week():
    d = dt.now()
    monday = d - td(days=d.weekday())
    begin = [monday + td(days=day) for day in range(7)][0]
    end = [monday + td(days=day) for day in range(7)][6]
    return [begin.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')]
