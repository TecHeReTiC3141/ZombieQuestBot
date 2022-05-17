from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from asyncio import sleep
from datetime import datetime
import json
import sqlite3

storage = MemoryStorage()

bot = Bot('5366480092:AAGkFZjXl47IT9Ltp13UCB3onnXh9zPAEU4')

disp = Dispatcher(bot, storage=storage)

db = sqlite3.connect('..\DB for quest.db')
cursor = db.cursor()

