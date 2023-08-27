from bot import bot, dp
from db import dillers
from funcs.decorators import check_admin_bot
from funcs import check_type, check_msg, dt
from texts import diller

from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


class NewDiller(StatesGroup):
    name = State()
    phone = State()
    address = State()


class ShowDiller(StatesGroup):
    name = State()


@check_admin_bot
@dp.message_handler(commands='new_diller')
async def new_diller(m: Message):
    await bot.send_message(m.chat.id, diller.New.start)
    await bot.send_message(m.chat.id, diller.cancel_msg)
    await bot.send_message(m.chat.id, diller.New.send_name)
    await NewDiller.name.set()


@dp.message_handler(state=NewDiller.name)
async def new_diller_get_name(m: Message, state: FSMContext):
    answer = m.text.strip()
    if check_msg.check_cancel(answer):
        await bot.send_message(m.chat.id, diller.New.cancel)
        await state.finish()
    else:
        if dillers.check_exists_diller(answer):
            await bot.send_message(m.chat.id, diller.New.diller_exists)
            await bot.send_message(m.chat.id, diller.New.send_name)
            await bot.send_message(m.chat.id, diller.cancel_msg)
            await NewDiller.name.set()
        else:
            await state.update_data(name=answer)
            await bot.send_message(m.chat.id, diller.New.send_phone)
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
    ...
