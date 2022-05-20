import sqlite3

import random

from aiogram import Bot, Dispatcher, executor
from aiogram.types import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot('5366480092:AAGkFZjXl47IT9Ltp13UCB3onnXh9zPAEU4')

disp = Dispatcher(bot, storage=storage)

db = sqlite3.connect('..\DB for quest.db')
cursor = db.cursor()
