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
    await message.answer('Хочешь начать квест?', reply_markup=keyboard)


async def start_quest(callback_query: CallbackQuery):
    await bot.send_message(callback_query.from_user.id,
                           'У вас будет 1 жизнь. При смерти нужно поиграть в игру для продолжения или начать все заново')
    await bot.send_message(callback_query.from_user.id, '''Какой-то биологический вирус поразил весь наш мир за считанные дни, люди превратились в беспощадных монстров пожирающих обычных людей. Когда всё это только начиналось я отправился в поход совсем один буквально на пару дней чтобы доказать себе, что я смогу выжить в одиночку. Наверное, именно это и спасло мне жизнь ведь сейчас города это рассадники зомби, в которых практически невозможно выжить.
     С момента моего выхода из глуши и начинается моя история.''')

    keyboard = InlineKeyboardMarkup()

    cursor.execute('''UPDATE User
                        SET prev_event = 0, cur_event = 0, life = 1, shooting = false, stealth = false
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

    if event_id == '21':
        cursor.execute('''UPDATE User
                        SET shooting = true
                        WHERE user_id = (?)''', (query.from_user.id,))

    elif event_id == '23':
        cursor.execute('''UPDATE User
                                SET stealth = true
                                WHERE user_id = (?)''', (query.from_user.id,))

    elif event_id == '61':
        cursor.execute('''SELECT shooting
                        FROM User
                        WHERE user_id = (?)''', (query.from_user.id,))
        shooting, = cursor.fetchone()
        if shooting:
            event_id += '1'
        else:
            event_id += '2'

    elif event_id == '62':
        cursor.execute('''SELECT stealth
                                FROM User
                                WHERE user_id = (?)''', (query.from_user.id,))
        stealth, = cursor.fetchone()
        if stealth:
            event_id += '1'
        else:
            event_id += '2'

    elif event_id == '51':
        cursor.execute('''SELECT shooting
                                FROM User
                                WHERE user_id = (?)''', (query.from_user.id,))
        shooting, = cursor.fetchone()
        if shooting:
            event_id += '1'
        else:
            event_id += '2'

    elif event_id == '53':
        cursor.execute('''SELECT stealth
                                FROM User
                                WHERE user_id = (?)''', (query.from_user.id,))
        stealth, = cursor.fetchone()
        if stealth:
            event_id += '1'
        else:
            event_id += '2'

    elif event_id == '62':
        cursor.execute('''SELECT stealth
                                FROM User
                                WHERE user_id = (?)''', (query.from_user.id,))
        stealth, = cursor.fetchone()
        if stealth:
            event_id += '1'
        else:
            event_id += '2'
    print(event_id)

    cursor.execute('''SELECT text, image, audio, death
                            FROM Event
                            WHERE Event_id = (?);''', (event_id,))  # get event

    text, image, audio, death = cursor.fetchone()



    if image:
        try:
            with open(fr'..\images\{image}.jpg', 'rb') as photo:
                await query.message.answer_photo(photo)
        except Exception as e:
            print(e)

    if audio:
        try:
            with open(audio, 'rb') as aud:
                await query.message.answer_voice(aud)
        except Exception as e:
            print(e)

    cursor.execute('''SELECT life 
                    FROM User
                    WHERE user_id = (?)''', (query.from_user.id,))  # checking left lives
    life, = cursor.fetchone()

    if life == 0:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton(text='В самое начало', callback_data='again'))
        keyboard.row(InlineKeyboardButton(text='Начать игру?', callback_data='request_game'))

        keyboard.row(InlineKeyboardButton(text='Со мной', callback_data='game_with_bot'),
                     InlineKeyboardButton(text='Со другим игроком', callback_data='game_with_user'))
        await bot.send_message(query.from_user.id, '''К сожалению, у вас кончились жизни. Чтобы их восстановить, вам нужно сыграть в игру с другим пользователем или со мной
                        Начать игру?''', reply_markup=keyboard)

    elif death:
        await bot.send_message(query.from_user.id, text)

        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton(text='В самое начало?', callback_data='again'))

        keyboard.row(InlineKeyboardButton(text='Начать игру?', callback_data='request_game'))

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
    await query.message.delete()


async def start_game_with_bot(query: CallbackQuery):
    max_val = random.choice([100, 1000, 5000, 10000])

    cursor.execute('''UPDATE User
                    SET num_for_game = (?)
                    WHERE user_id = (?)''', (random.randint(1, max_val), query.from_user.id))
    await bot.send_message(query.from_user.id, f'''Я загадал случайное число от 1 до {max_val}.
    Тебе нужно его угадать. Удачи''')
    await Quest_states.game.set()

    db.commit()
    await query.message.delete()


async def game_with_bot(message: Message):
    try:
        guess = int(message.text)

        cursor.execute('''SELECT num_for_game
                            FROM User
                            Where user_id = (?)''', (message.from_user.id,))

        right, = cursor.fetchone()
        print(guess, right)
        if right == guess:

            cursor.execute('''UPDATE User
                            SET life = 1
                            WHERE user_id = (?)''', (message.from_user.id,))

            await Quest_states.quest.set()

            keyboard = InlineKeyboardMarkup()

            cursor.execute('''SELECT cur_event
                                        FROM User
                                        WHERE user_id = (?)''', (message.from_user.id,))

            event_id, = cursor.fetchone()
            print(event_id)

            keyboard.row(InlineKeyboardButton(text='Продолжить', callback_data=f'event {event_id}'))
            await message.answer('Вы угадали!', reply_markup=keyboard)

        elif right < guess:
            await message.answer('Загаданное число меньше')
        else:
            await message.answer('Загаданное число больше')

    except Exception as e:
        await message.answer('Пожалуйста, введите число')
        print(e)
