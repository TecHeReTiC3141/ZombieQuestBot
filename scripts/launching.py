from client_hadlers import *
from game_for_reviving import *


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать квест"),
    ]
    await bot.set_my_commands(commands)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands='start', state='*')
    dp.register_callback_query_handler(start_quest, text='start_quest', state='*')
    dp.register_callback_query_handler(miss_quest, text='miss_quest')
    dp.register_callback_query_handler(go_to_event, text_startswith='event', state='*')
    dp.register_callback_query_handler(revive, text='return', state='*')
    dp.register_callback_query_handler(again, text='again', state='*')
    dp.register_callback_query_handler(start_game_with_bot, text='game_with_bot')
    dp.register_message_handler(game_with_bot, state=Quest_states.game)


async def on_start(_):
    print('Bot is online')
    register_handlers(disp)
    await set_commands(bot)


executor.start_polling(disp, skip_updates=True, on_startup=on_start)
