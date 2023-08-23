from handlers import client, admin, other
from aiogram.utils import executor

from create_bot import dp
from db import sql_start


async def on_startup(_):
    print('Бот вышел онлайн')
    sql_start.sql_start()


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
