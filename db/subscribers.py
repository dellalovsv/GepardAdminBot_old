from . import query
from funcs import dt
from funcs.check_type import check_int

from netaddr import IPAddress


class Abon:
    def __init__(self, uid: str | int = None):
        self.uid = uid

    def get_login(self) -> str | bool | None:
        try:
            sql = 'select id as login from users where uid=%s'
            res = query(sql, self.uid)
            if res is not False and res is not None and len(res) > 0:
                return res[0]['login']
            else:
                return None
        except Exception as e:
            print(f'ABONS.GET_LOGIN (ERROR): {e}')
            return False

    def get_address(self) -> str | bool | None:
        try:
            sql = 'select address_street as street, address_build as build from users_pi where uid=%s'
            res = query(sql, self.uid)
            if res is not False and res is not None and len(res) > 0:
                if check_int(res[0]['street']):
                    street = res[0]['street']
                    build = res[0]['build']
                    sql = 'select number from builds where id=%s and street_id=%s'
                    res = query(sql, build, street)
                    if res is not None and res is not False and len(res) > 0:
                        build = res[0]['number']
                        sql = 'select name, district_id from streets where id=%s'
                        res = query(sql, street)
                        if res is not None and res is not False and len(res) > 0:
                            street = res[0]['name']
                            district = res[0]['district_id']
                            sql = 'select name from districts where id=%s'
                            res = query(sql, district)
                            if res is not None and res is not False and len(res) > 0:
                                district = res[0]['name']
                                return f'{district}; {street}, {build}'

            return None
        except Exception as e:
            print(f'ABON.GET_ADDRESS (ERROR): {e}')
            return False


class Payment:
    def __init__(self, uid: str | int = None):
        self.uid = uid

    def get_first_payment(self) -> dict | int | None:
        try:
            sql = ('select date, sum, last_deposit, ip, ext_id, inner_describe from payments where uid=%s and method=2 '
                   'order by date asc limit 1')
            res = query(sql, self.uid)
            if res is not None and res is not False and len(res) > 0:
                res[0]['date'] = dt.conv_date(str(res[0]['date']))
                res[0]['sum'] = "%.2f" % float(res[0]['sum'])
                res[0]['last_deposit'] = "%.2f" % float(res[0]['last_deposit'])
                res[0]['ip'] = str(IPAddress(res[0]['ip']))
                if len(res[0]['ext_id']) > 0:
                    res[0]['card'] = res[0]['ext_id']
                    res[0].pop('ext_id')
                    res[0].pop('inner_describe')
                    return res[0]
                else:
                    res[0]['card'] = res[0]['inner_describe']
                    res[0].pop('ext_id')
                    res[0].pop('inner_describe')
                    return res[0]

            return None
        except Exception as e:
            print(f'PAYMENTS.GET_LAST_PAYMENT (ERROR): {e}')
            return -1

    def get_last_payment(self) -> dict | int | None:
        try:
            sql = ('select date, sum, last_deposit, ip, ext_id, inner_describe from payments where uid=%s and method=2 '
                   'order by date desc limit 1')
            res = query(sql, self.uid)
            if res is not None and res is not False and len(res) > 0:
                res[0]['date'] = dt.conv_date(str(res[0]['date']))
                res[0]['sum'] = "%.2f" % float(res[0]['sum'])
                res[0]['last_deposit'] = "%.2f" % float(res[0]['last_deposit'])
                res[0]['ip'] = str(IPAddress(res[0]['ip']))
                if len(res[0]['ext_id']) > 0:
                    res[0]['card'] = res[0]['ext_id']
                    res[0].pop('ext_id')
                    res[0].pop('inner_describe')
                    return res[0]
                else:
                    res[0]['card'] = res[0]['inner_describe']
                    res[0].pop('ext_id')
                    res[0].pop('inner_describe')
                    return res[0]

            return None
        except Exception as e:
            print(f'PAYMENTS.GET_LAST_PAYMENT (ERROR): {e}')
            return -1

    def get_all_payments(self) -> list[tuple] | int | None:
        try:
            sql = 'select date, sum, last_deposit, ip, ext_id, inner_describe from payments where uid=%s and method=2'
            res = query(sql, self.uid)
            if res is not None and res is not False and len(res) > 0:
                i = 0
                while i < len(res):
                    res[i]['date'] = dt.conv_date(str(res[i]['date']))
                    res[i]['sum'] = "%.2f" % float(res[i]['sum'])
                    res[i]['last_deposit'] = "%.2f" % float(res[i]['last_deposit'])
                    res[i]['ip'] = str(IPAddress(res[i]['ip']))
                    res[i]['card'] = res[i]['ext_id'] if len(res[i]['ext_id']) else res[i]['inner_describe']
                    res[i].pop('ext_id')
                    res[i].pop('inner_describe')
                    i += 1
                return res

            return None
        except Exception as e:
            print(f'SUBCRIBE.PAYMENT.GET_ALL_PAYMENTS (ERROR): {e}')
            return -1
