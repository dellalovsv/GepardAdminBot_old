import logging

import config

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())
