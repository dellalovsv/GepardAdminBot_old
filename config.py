import os

from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

CURRENCY = os.getenv("CURRENCY")

COUNT_SYMBOLS_OF_SERIAL_CARD = int(os.getenv("COUNT_SYMBOLS_OF_SERIAL_CARD"))
COUNT_LITTERS_OF_SERIAL_CARD = int(os.getenv("COUNT_LITTERS_OF_SERIAL_CARD"))
COUNT_NUMBERS_OF_SERIAL_CARD = int(os.getenv("COUNT_NUMBERS_OF_SERIAL_CARD"))
