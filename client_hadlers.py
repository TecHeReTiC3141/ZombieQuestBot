import types

from bot import *

async def start(message: types.Message):

    cursor.execute('''INSERT INTO User (name, user_id)
                    VALUES (?, ?)''', (message.from_user.username, message.from_user.id))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row([types.InlineKeyboardButton(text='Да', callback_data='start_quest'),
                  types.InlineKeyboardButton(text='Нет', callback_data='miss_quest')])

    await message.answer('Приветствую 👋')
    await message.answer('Хочешь начать квест', reply_markup=keyboard)

async def start_quest(message: types.Message):

    await message.reply('Отлично')
