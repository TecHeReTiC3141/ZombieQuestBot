import types

from scripts.bot import *


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


async def start_quest(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    cursor.execute('''SELECT text
                        FROM Event
                        WHERE Event_id = (SELECT cur_event
                                          FROM User
                        WHERE user_id = (?));''', (callback_query.from_user.id,))
    text, = cursor.fetchone()
    cursor.execute('''SELECT to_id, Refs.text
                        FROM Event JOIN Refs ON Event.Event_id = Refs.from_id
                        WHERE Event_id = (SELECT cur_event
                                          FROM User
                        WHERE user_id = (?));''', (callback_query.from_user.id,))
    events = cursor.fetchall()
    print(events, text)
    for event in events:
        keyboard.row(types.InlineKeyboardButton(text=event[1], callback_data=f'event {event[0]}'))

    await bot.send_message(callback_query.from_user.id, 'Отлично. Начинаем...')
    await bot.send_message(callback_query.from_user.id, text, reply_markup=keyboard)
    await callback_query.answer()


#@disp.callback_query_handler(text_startswith="event")
async def go_to_event(callback_query: types.CallbackQuery):

    print(callback_query.data, callback_query.message)

async def miss_quest(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Пока')
