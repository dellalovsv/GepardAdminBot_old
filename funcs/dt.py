from datetime import datetime as dt


def get_date(time: bool = False) -> str:
    if time:
        return dt.now().strftime('%d.%m.%Y %H:%M:%S')
    else:
        return dt.now().strftime('%d.%m.%Y')
