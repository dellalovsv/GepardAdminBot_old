from bot import bot, dp
from funcs.decorators import check_admin_bot
from funcs import dt
from texts import menu

from aiogram.types import Message


@dp.message_handler(commands=['start', 'help'])
@check_admin_bot
async def start(m: Message):
    await bot.send_message(m.chat.id, menu.menu % (dt.get_date(True)))
