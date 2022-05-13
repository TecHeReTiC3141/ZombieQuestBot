from client_hadlers import *
from fsm_content import *

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')
    dp.register_message_handler(start_quest, callback='start_quest')

async def on_start(_):
    print('Bot is online')
    register_handlers(disp)

executor.start_polling(disp, skip_updates=True, on_startup=on_start)