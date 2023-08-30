from bot import bot, dp
from db import dillers
from funcs.decorators import check_admin_bot
from funcs import check_msg, dt
from texts import diller

from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


# Класс для Middleware (Добавление нового диллера)
class NewDiller(StatesGroup):
    name = State()
    phone = State()
    address = State()


# Класс для Middleware (Отображения диллера по имени)
class ShowDiller(StatesGroup):
    name = State()


# Добавление нового диллера
@check_admin_bot
@dp.message_handler(commands='new_diller')
async def new_diller(m: Message):
    await bot.send_message(m.chat.id, diller.New.start)
    await bot.send_message(m.chat.id, diller.cancel_msg)
    await bot.send_message(m.chat.id, diller.New.send_name)
    await NewDiller.name.set()


# Получение названия дллера
@dp.message_handler(state=NewDiller.name)
async def new_diller_get_name(m: Message, state: FSMContext):
    answer = m.text.strip()
    # Проверка на отправку команды отмены
    if check_msg.check_cancel(answer):
        # Команда получена, действие отменено
        await bot.send_message(m.chat.id, diller.New.cancel)
        await state.finish()
    else:
        # Проверка существования диллера при получении названия нового диллера
        if dillers.check_exists_diller(answer):
            # Диллер существует
            await bot.send_message(m.chat.id, diller.New.diller_exists)
            await bot.send_message(m.chat.id, diller.New.send_name)
            await bot.send_message(m.chat.id, diller.cancel_msg)
            await NewDiller.name.set()
        else:
            # Диллер не существует
            await state.update_data(name=answer)
            # Отправка сообщения с запросом № телефона
            await bot.send_message(m.chat.id, diller.New.send_phone)
            # Переход к следующеей переменной
            await NewDiller.next()


@dp.message_handler(state=NewDiller.phone)
async def new_diller_get_phone(m: Message, state: FSMContext):
    answer = m.text.strip()
    if check_msg.check_cancel(answer):
        await bot.send_message(m.chat.id, diller.New.cancel)
        await state.finish()
    else:
        await state.update_data(phone=answer)
        await bot.send_message(m.chat.id, diller.New.send_address)
        await NewDiller.next()


@dp.message_handler(state=NewDiller.address)
async def new_diller_get_phone(m: Message, state: FSMContext):
    answer = m.text.strip()
    if check_msg.check_cancel(answer):
        await bot.send_message(m.chat.id, diller.New.cancel)
        await state.finish()
    else:
        await state.update_data(address=answer)
        data = await state.get_data()
        if dillers.new_diller(data['name'], data['address'], data['phone']):
            await bot.send_message(m.chat.id, diller.New.success)
        else:
            await bot.send_message(m.chat.id, diller.New.error)
        await state.finish()


@check_admin_bot
@dp.message_handler(commands='show_diller')
async def show_diller(m: Message):
    await bot.send_message(m.chat.id, diller.Show.question)
    await bot.send_message(m.chat.id, diller.cancel_msg)
    await ShowDiller.name.set()


@dp.message_handler(state=ShowDiller.name)
async def show_diller_get(m: Message, state: FSMContext):
    answer = m.text.strip()
    if check_msg.check_cancel(answer):
        await state.finish()
        await bot.send_message(m.chat.id, diller.Show.cancel)
    else:
        if answer == '/all':
            await state.finish()
            res = dillers.show()
            if res != -1 and res is not None and len(res) > 0:
                msg = diller.Show.title_all
                i = 0
                while i < len(res):
                    res[i]['date_add'] = dt.conv_date(str(res[i]['date_add']))
                    msg += '\n\n' + diller.Show.diller % (
                        res[i]['id'],
                        res[i]['name'],
                        res[i]['phone'],
                        res[i]['address'],
                        "Активен" if res[i]['disable'] == 0 else "Заблокирован",
                        res[i]['date_add']
                    )
                    if len(msg) > 3000:
                        await bot.send_message(m.chat.id, msg)
                        msg = ''
                    i += 1
                if len(msg) > 0:
                    await bot.send_message(m.chat.id, msg)
            else:
                await bot.send_message(m.chat.id, diller.Show.dillers_not_found)
        else:
            res = dillers.show(answer)
            if res is not None and res != -1 and len(res) > 0:
                msg = diller.Show.title_one
                i = 0
                while i < len(res):
                    res[i]['date_add'] = dt.conv_date(str(res[i]['date_add']))
                    msg += '\n\n' + diller.Show.diller % (
                        res[i]['id'],
                        res[i]['name'],
                        res[i]['phone'],
                        res[i]['address'],
                        "Активен" if res[i]['disable'] == 0 else "Заблокирован",
                        res[i]['date_add']
                    )
                    i += 1
                await bot.send_message(m.chat.id, msg)
                await state.finish()
            else:
                await state.finish()
                await bot.send_message(m.chat.id, diller.Show.dillers_not_found)

