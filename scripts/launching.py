from client_hadlers import *
from fsm_content import *

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать квест"),
    ]
    await bot.set_my_commands(commands)



def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')
    dp.register_callback_query_handler(start_quest, text='start_quest')
    dp.register_callback_query_handler(miss_quest, text='miss_quest')
    dp.register_callback_query_handler(go_to_event, text_startswith='event')
    dp.register_callback_query_handler(revive, text='return')
    dp.register_callback_query_handler(again, text='again')


async def on_start(_):
    print('Bot is online')
    register_handlers(disp)
    await set_commands(bot)


executor.start_polling(disp, skip_updates=True, on_startup=on_start)
