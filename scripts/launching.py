from client_hadlers import *
from fsm_content import *


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')
    dp.register_callback_query_handler(start_quest, text='start_quest')
    dp.register_callback_query_handler(miss_quest, text='miss_quest')
    dp.register_callback_query_handler(go_to_event, text_startswith='event')
    dp.register_callback_query_handler(revive, text='return')


async def on_start(_):
    print('Bot is online')
    register_handlers(disp)


executor.start_polling(disp, skip_updates=True, on_startup=on_start)
