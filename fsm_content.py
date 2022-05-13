from bot import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class QuestState(StatesGroup):
    greeting = State()
    quest = State()
    end = State()
