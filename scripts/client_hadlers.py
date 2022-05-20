from scripts.bot import *
from scripts.game_for_reviving import *


def get_keyboard(events: tuple) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for event in events:
        keyboard.row(InlineKeyboardButton(text=event[1], callback_data=f'event {event[0]}'))
    return keyboard


async def start(message: Message):
    await bot.send_message(1699660434,
                           f'User {message.from_user.username if message.from_user.username else message.from_user.first_name} connected.')
    try:
        cursor.execute('''INSERT INTO User (name, user_id)
                    VALUES (?, ?)''', (message.from_user.username if message.from_user.username
                                                              else message.from_user.first_name, message.from_user.id))
    except Exception as e:
        print(e)

    cursor.execute('''SELECT COUNT(*)
                        FROM User''')

    await bot.send_message(1699660434,
                           f'There are {cursor.fetchone()[0]} at all.')

    keyboard = InlineKeyboardMarkup()
    keyboard.row(*[InlineKeyboardButton(text='Да', callback_data='start_quest'),
                   InlineKeyboardButton(text='Нет', callback_data='miss_quest')])

    await message.answer('Приветствую 👋')
    await message.answer('Хочешь начать квест', reply_markup=keyboard)


async def start_quest(callback_query: CallbackQuery):
    await bot.send_message(callback_query.from_user.id,
                           'У вас будет 3 жизни. Если они кончаются, то нужно их восстановить для продолжения или начать все заново')
    await bot.send_message(callback_query.from_user.id, '''Какой-то биологический вирус поразил весь наш мир за считанные дни, люди превратились в беспощадных монстров пожирающих обычных людей. Когда всё это только начиналось я отправился в поход совсем один буквально на пару дней чтобы доказать себе, что я смогу выжить в одиночку. Наверное, именно это и спасло мне жизнь ведь сейчас города это рассадники зомби, в которых практически невозможно выжить.
     С момента моего выхода из глуши и начинается моя история.''')

    keyboard = InlineKeyboardMarkup()

    cursor.execute('''UPDATE User
                        SET prev_event = 0, cur_event = 0, life = 1
                        WHERE user_id = (?);
                        ''', (callback_query.from_user.id,))  # erasing user's progress

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
    cursor.execute('''SELECT text, image, audio, death
                            FROM Event
                            WHERE Event_id = (?);''', (event_id,))  # get event

    text, image, audio, death = cursor.fetchone()

    if image:
        try:
            with open(fr'..\images\{image}.jpg', 'rb') as photo:
                await query.message.reply_photo(photo)
        except Exception as e:
            print(e)

    if death:
        await bot.send_message(query.from_user.id, text)

        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton(text='В самое начало', callback_data='again'))

        cursor.execute('''SELECT life 
                        FROM User
                        WHERE user_id = (?)''', (query.from_user.id,))
        life, = cursor.fetchone()  # checking left lives

        if life > 0:
            keyboard.row(InlineKeyboardButton(text='Назад', callback_data='return'))
            await bot.send_message(query.from_user.id, 'Кажется, вы мертвы, вернуться назад?', reply_markup=keyboard)
        else:
            keyboard.row(InlineKeyboardButton(text='Начать игру', callback_data='request_game'))

            keyboard.row(InlineKeyboardButton(text='Со мной', callback_data='game_with_bot'),
                         InlineKeyboardButton(text='Со другим игроком', callback_data='game_with_user'))
            await bot.send_message(query.from_user.id, '''К сожалению, у вас кончились жизни. Чтобы их восстановить, вам нужно сыграть в игру с другим пользователем или со мной
                Начать игру?''', reply_markup=keyboard)

    else:
        cursor.execute('''UPDATE User
                        SET prev_event = cur_event, cur_event = (?)
                        WHERE user_id = (?);
                        ''', (event_id, query.from_user.id))  # updating user event

        cursor.execute('''SELECT to_id, Refs.text
                                FROM Event JOIN Refs ON Event.Event_id = Refs.from_id
                                WHERE Event_id = (SELECT cur_event
                                                  FROM User
                                WHERE user_id = (?));''', (query.from_user.id,))  # getting further events
        keyboard = get_keyboard(cursor.fetchall())

        await bot.send_message(query.from_user.id, text, reply_markup=keyboard)
        db.commit()

    await query.answer()
    await query.message.delete()
    print(query.data, query.message)


async def miss_quest(callback_query: CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Пока')


async def revive(query: CallbackQuery):
    print((query.from_user.id,))
    cursor.execute('''SELECT cur_event
                            FROM User
                            WHERE user_id = (?)''', (query.from_user.id,))

    event_id, = cursor.fetchone()

    cursor.execute('''SELECT text, image, audio, death
                                FROM Event
                                WHERE Event_id = (?);''', (event_id,))  # get event

    text, image, audio, death = cursor.fetchone()

    cursor.execute('''UPDATE User
                            SET prev_event = cur_event, cur_event = (?), life = life - 1
                            WHERE user_id = (?);
                            ''', (event_id, query.from_user.id))  # updating user event

    cursor.execute('''SELECT to_id, Refs.text
                                    FROM Event JOIN Refs ON Event.Event_id = Refs.from_id
                                    WHERE Event_id = (SELECT cur_event
                                                      FROM User
                                    WHERE user_id = (?));''', (query.from_user.id,))  # getting further events
    keyboard = get_keyboard(cursor.fetchall())

    await bot.send_message(query.from_user.id, text, reply_markup=keyboard)
    db.commit()

    await query.answer()
    await query.message.delete()


async def again(query: CallbackQuery):
    await start_quest(query)


async def game(message: Message, context: FSMContext):
    pass
