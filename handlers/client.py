from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove

from create_bot import bot
from keyboards import kb_client
from db import sql_start


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Приятного аппетита', reply_markup=kb_client)
        # message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему: https://t.me/MVPPizzaBot')


# @dp.message_handler(commands=['Режим'])
async def pizza_open_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вт-Чт с 9:00 до 20:00, Пт-Сб с 10:00 до 23:00')


# @dp.message_handler(commands=['Расположение'])
async def pizza_place_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'ул. Центральная, д. 1', reply_markup=ReplyKeyboardRemove())


# # @dp.message_handler(commands=['Меню'])
async def pizza_menu_command(message: types.Message):
    await sql_start.sql_read(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(pizza_open_command, commands=['Режим'])
    dp.register_message_handler(pizza_place_command, commands=['Расположение'])
    dp. register_message_handler(pizza_menu_command, commands=['Меню'])
