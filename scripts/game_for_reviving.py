from bot import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class Quest_states(StatesGroup):
    quest = State()
    game = State()
