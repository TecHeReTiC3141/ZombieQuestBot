import sqlite3

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot('5366480092:AAGkFZjXl47IT9Ltp13UCB3onnXh9zPAEU4')

disp = Dispatcher(bot, storage=storage)

db = sqlite3.connect('..\DB for quest.db')
cursor = db.cursor()

