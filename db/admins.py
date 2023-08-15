from . import query


class Bot:
    def __init__(self, tid: int):
        self.id = tid

    def check_admin(self) -> bool | int:
        try:
            sql = 'select tid from bot_admins_telegram where tid=%s and disable=0'
            res = query(sql, self.id)
            if res is not False and res is not None and len(res) > 0:
                if res[0]['tid'] == self.id:
                    return True
            else:
                return False
        except Exception as e:
            print(f'DB.ADMINS.CHECK_ADMIN (ERROR): {e}')
            return -1
