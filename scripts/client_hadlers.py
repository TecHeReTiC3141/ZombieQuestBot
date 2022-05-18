from scripts.bot import *


def get_keyboard(events: tuple) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for event in events:
        keyboard.row(InlineKeyboardButton(text=event[1], callback_data=f'event {event[0]}'))
    return keyboard


async def start(message: Message):
    try:
        cursor.execute('''INSERT INTO User (name, user_id)
                    VALUES (?, ?)''', (message.from_user.username, message.from_user.id))
    except Exception as e:
        print(e)

    keyboard = InlineKeyboardMarkup()
    keyboard.row(*[InlineKeyboardButton(text='Да', callback_data='start_quest'),
                   InlineKeyboardButton(text='Нет', callback_data='miss_quest')])

    await message.answer('Приветствую 👋')
    await message.answer('Хочешь начать квест', reply_markup=keyboard)


async def start_quest(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup()

    cursor.execute('''UPDATE User
                        SET prev_event = 0, cur_event = 0
                        WHERE user_id = (?);
                        ''', (callback_query.from_user.id,)) # erasing user's progress

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
        keyboard.row(InlineKeyboardButton(text=event[1], callback_data=f'event {event[0]}'))

    await bot.send_message(callback_query.from_user.id, 'Отлично. Начинаем...')
    await bot.send_message(callback_query.from_user.id, text, reply_markup=keyboard)
    await callback_query.answer()


# @disp.callback_query_handler(text_startswith="event")
async def go_to_event(query: CallbackQuery):
    event_id = query.data.split()[1]
    cursor.execute('''SELECT text, image, audio
                            FROM Event
                            WHERE Event_id = (?);''', (event_id,))  # get event



    text, image, audio = cursor.fetchone()

    cursor.execute('''UPDATE User
                    SET prev_event = cur_event, cur_event = (?)
                    WHERE user_id = (?);
                    ''', (event_id, query.from_user.id))  # updating user event

    cursor.execute('''SELECT to_id, Refs.text
                            FROM Event JOIN Refs ON Event.Event_id = Refs.from_id
                            WHERE Event_id = (SELECT cur_event
                                              FROM User
                            WHERE user_id = (?));''', (query.from_user.id,)) # getting further events
    keyboard = get_keyboard(cursor.fetchall())


    await bot.send_message(query.from_user.id, text, reply_markup=keyboard)
    db.commit()

    await query.answer()
    await query.message.delete()
    print(query.data, query.message)


async def miss_quest(callback_query: CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Пока')
