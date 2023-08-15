from . import success_ico, cancel_ico, error_ico, money_ico, dollar_ico, cancel_msg, cancel_set_msg
import config


class New(object):
    type_rec = {
        1: 'Доход ➕',
        2: 'Расход ➖'
    }

    start = '<b>Начата процедура добавления нового "Доход/Расход".</b>'
    get_type = 'Выбери тип <b>/1 Доход</b> или <b>/2 Расход</b>.'
    get_summa = 'Отправь <b>сумму</b>.'
    get_dsc = 'Отправь <b>описание</b> записи.'

    no_slash_in_msg = f'{error_ico}\nОтправь команду <b>/1 - Доход</b> или <b>/2 - Расход</b>!'
    error_answer_type_rec = (f'{error_ico}\nКоманда должна содержать число!\n'
                             f'/1 - Доход</b> или <b>/2 - Расход</b>.\n'
                             f'<b>Отправь одну из выше указанных команд.</b>')
    error_answer_summa = (f'{error_ico}\nСумма должна быть цифрами.\n'
                          f'<b>Отправь повторно сумму.</b>')

    check_data = ('<b>Все ли данные верны?</b>\n\n'
                  '<b>Тип</b>: %s\n'
                  f'<b>Сумма</b>: %s {config.CURRENCY}\n'
                  '<b>Описание</b>: %s\n\n'
                  '<b>/yes</b> - Да, данные верны.\n'
                  '<b>/no</b> - Нет данные не верны.')
    check_data_error = (f'{cancel_ico}\n<b>Так как ты указал, что данные не верны, процедура будет начата с начала. '
                        'Отправь повторно "/new_finance" для повтора операции.</b>')

    get_cancel = cancel_msg
    set_cancel = cancel_set_msg

    success = f'{success_ico}\n<b>%s</b> успешно завершено.'
    cancel = f'{cancel_ico}\nОперация добавления <b>%s</b> отменена!'
    error = (f'{error_ico}\n<b>В процессе текущей операции произошла ошибка!'
             f'Отправь повторно команду "/new_finance", чтобы повторить процедуру.</b>')


class Show(object):
    start = ('Отправь <b>/all - Показать все расходы/доходы</b>, <b>/last_week - Показать доходы/расходы'
             ' за последнюю неделю</b> или <b>/of_date - Показать доходы/расходы с даты по дату</b>.')

    get_begin_date = 'Отправь <b>начальную дату.</b>'
    get_end_date = 'Отправь <b>конечную дату.</b>'

    title_last_week = f'{money_ico}\n<b>Доходы/Расходы за последнюю неделю (с %s по %s):</b>'
    title_all = f'{money_ico}\n<b>Доходы/Расходы за весь период:</b>'
    title_of_date = f'{money_ico}\n<b>Доходы/Расходы за период с %s по %s:</b>'

    msg = ('<b>Дата:</b> %s\n'
           '<b>Тип:</b> %s\n'
           f'<b>Сумма:</b> %s {config.CURRENCY}\n'
           '<b>Описание:</b> %s')

    summa_dohod_rashod = (f'{dollar_ico}\n<b>Общая сумма доходов и расходов:</b>\n'
                          f'Доход: <b>%s</b> {config.CURRENCY}\n'
                          f'Раход: <b>%s</b> {config.CURRENCY}\n'
                          f'Всего: <b>%s</b> {config.CURRENCY}')

    records_not_found = f'{error_ico}\nЗаписей не найдено!'

    error_command = (f'{error_ico}\n<b>Ты отправил не верную команду!</b>\n'
                     f'Отправь одну из команд из сообщения ниже!')
    error_date = (f'{error_ico}\nТы отправил не верную дату. Начальная дата не может быть больше сегодняшней\n'
                  f'<b>Повтори попытку снова!</b>')
    error_type_date = f'{error_ico}\nДата должна быть в формате <b>dd.mm.yyyy</b>!\nПопробуй повторно отправить дату.'
    cancel_msg = f'{cancel_ico}\n<b>Текущая операция была отменена!</b>'
