from db import admins

from aiogram.types import Message


def check_admin_bot(func):
    def wrapper(m: Message):
        if admins.Bot(m.from_user.id).check_admin():
            return func(m)
    return wrapper
