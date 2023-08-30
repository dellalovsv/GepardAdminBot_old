from . import error_ico, cancel_ico, success_ico, cancel_set_msg, cancel_msg, warning_ico


class New(object):
    start = 'Начата процедура <b>Добавление нового диллера</b>!'

    send_name = 'Отправь <b>Название диллера</b>.'
    send_address = 'Отправь <b>Адрес диллера</b>.'
    send_phone = 'Отправь <b>№ телефона диллера</b> в формате: <b>+7 (код) № телефона</b>.'

    success = (f'{success_ico}\n'
               f'<b>Добавление нового диллера успешно завершено!</b>')
    diller_exists = (f'{warning_ico}\n'
                     f'<b>Диллер с таким название уже существует.</b>')
    error = (f'{error_ico}\n'
             f'<b>Произошла ошибка при добавлении нового диллера</b>')
    cancel = f'{cancel_set_msg % "Добавление нового диллера"}'


class Show(object):
    title_all = '<b>Подробная информация о диллерах</b>'
    title_one = '<b>Подробная информация о диллере</b>'
    diller = ('ID: <b>/%s</b>\n'
              'Название: <b>%s</b>\n'
              '№ Телефона: <b>%s</b>\n'
              'Адрес: <b>%s</b>\n'
              'Состояние: <b>%s</b>\n'
              'Дата добавления: <b>%s</b>')
    diller_short = ('ID: <b>%s</b>\n'
                    'Название: <b>%s</b>')

    question = ('Если нужно показать всех диллеров, то отправь команду <b>/all</b>.\n'
                'Чтобы показать конкретного диллера, отправь <b>название</b>.')

    dillers_not_found = f'{warning_ico}\n<b>Нет ни одно диллера.</b>'
    cancel = (f'{cancel_ico}\n'
              f'<b>Отображение диллеров отменено!</b>')
