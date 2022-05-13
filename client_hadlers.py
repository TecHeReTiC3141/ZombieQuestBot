import types

from bot import *

async def start(message: types.Message):
    try:
        cursor.execute('''INSERT INTO User (name, user_id)
                    VALUES (?, ?)''', (message.from_user.username, message.from_user.id))
    except Exception as e:
        print(e)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(*[types.InlineKeyboardButton(text='Да', callback_data='start_quest'),
                  types.InlineKeyboardButton(text='Нет', callback_data='miss_quest')])

    await message.answer('Приветствую 👋')
    await message.answer('Хочешь начать квест', reply_markup=keyboard)


@disp.callback_query_handler(func=lambda c: c.data == 'start_quest')
async def start_quest(callback_query: types.CallbackQuery):

    await bot.send_message(callback_query.from_user.id, 'Отлично')


@disp.callback_query_handler(func=lambda c: c.data == 'miss_quest')
async def miss_quest(callback_query: types.CallbackQuery):

    await bot.send_message(callback_query.from_user.id, 'Пока')